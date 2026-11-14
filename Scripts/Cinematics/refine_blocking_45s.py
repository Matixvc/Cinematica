"""Refine existing 45s sequence only; backup first; no map/animation changes."""
import unreal as u
import json, math, time
from pathlib import Path
ROOT=Path(u.Paths.project_dir()); OUT=ROOT/'Saved/CinematicDirector'
DEST='/Game/Animacion/Cinematica/LS_Cameras_45s'
BACKUP=DEST+'_Backup_PreRefine'
lib=u.LevelSequenceEditorBlueprintLibrary
assets=u.EditorAssetLibrary
assert u.SystemLibrary.get_engine_version().startswith('5.6.1')
assert assets.does_asset_exist(DEST) and not assets.does_asset_exist(BACKUP), 'Missing sequence or backup already exists; stop and inspect.'
lib.close_level_sequence()
seq=u.load_asset(DEST)
assert assets.get_metadata_tag(seq,'CinematicDirectorOwner')=='blocking-45s-v1'
actors={a.get_actor_label():a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()}
assert '/Game/Animacion/Escenario/Escena.' in actors['Cam0'].get_path_name()
shots=json.loads((OUT/'shots_45s.json').read_text(encoding='utf-8'))
labels=['CAM00','CAM01','CAM02','CAM03','CAM03_1','CAM04','CAM05','CAM05_1','CAM06','CAM07','CAM08']
assert [s['label'] for s in shots]==labels
assert [(s['start'],s['end']) for s in shots]==list(zip([0,72,192,288,432,456,600,672,696,792,936],[72,192,288,432,456,600,672,696,792,936,1080]))
def xyz(v): return [v.x,v.y,v.z]
def add(a,b): return [x+y for x,y in zip(a,b)]
def sub(a,b): return [x-y for x,y in zip(a,b)]
def mul(a,k): return [x*k for x in a]
def norm(a): return math.sqrt(sum(x*x for x in a))
def unit(a): return mul(a,1/norm(a))
def blend(a,b,t): return add(a,mul(sub(b,a),t))
def center(n): return xyz(actors[n].get_actor_bounds(False)[0])
def loc(n): return xyz(actors[n].get_actor_location())
f=loc('BP_Father_ThirdPersonCharacter'); s=loc('BP_Son_ThirdPersonCharacter')
fh=add(f,[0,0,65]); head=center('Auriculares'); head[2]-=4
house=center('DogHouse_Base'); work=center('Lista_Madera_02_DogHouse'); hammer=center('SM_Hammer'); crate=center('WoodenCrate2')
mid=blend(f,s,.5); mid[2]=95
front=unit([shots[0]['position'][0]-mid[0],shots[0]['position'][1]-mid[1],0]); right=[front[1],-front[0],0]
def pos(t,d,h=0,side=0): return add(add(add(t,mul(front,d)),mul(right,side)),[0,0,h])
# Closer physical positions, preserving the established screen direction.
req=blend(fh,head,.30); req[2]=135
fr=blend(fh,work,.40); fr[2]=110
ten=blend(fh,house,.28); ten[2]=125
react=blend(head,fh,.20); react[2]=135
impact=[crate[0]-65,crate[1]+20,12]
detail=blend(work,hammer,.5)
# POV uses eye marker, looking between father and house, slightly above roof base.
povtarget=blend(house,fh,.32); povtarget[2]=105
plans={
'CAM01':(pos(mid,390,35),mid,35,5.6,mid),
'CAM02':(pos(req,310,10,-150),req,40,2.8,fh),
'CAM03':(pos(fr,255,25,-45),fr,45,5.6,fr),
'CAM03_1':(pos(detail,125,75,-45),detail,65,5.6,detail),
'CAM04':(pos(ten,280,15,-90),ten,40,5.6,fh),
'CAM05':(pos(mid,430,20,30),mid,35,8,mid),
'CAM05_1':(pos(impact,155,45,35),impact,55,5.6,impact),
'CAM06':(pos(react,265,0,135),react,45,4,head),
'CAM07':(pos(mid,400,35,-35),mid,35,5.6,mid),
'CAM08':(head,povtarget,28,8,povtarget),
}
# Resolve every section before changing anything. Original generator uses one track per property per actor.
bindings={b.get_name():b for b in seq.get_bindings()}
def section_at(track,sh):
    matches=[x for x in track.get_sections() if x.get_start_frame()==sh['start'] and x.get_end_frame()==sh['end']]
    assert len(matches)==1, (sh['label'],str(track),len(matches))
    return matches[0]
changes=[]
for sh in shots:
    name=sh['actor']; b=bindings['CD_CAM_'+name]; cb=bindings['CD_OPTICS_'+name]
    tr=[t for t in b.get_tracks() if isinstance(t,u.MovieScene3DTransformTrack)]; assert len(tr)==1
    sec=section_at(tr[0],sh); ch={str(c.channel_name):c for c in sec.get_all_channels()}
    optics={str(t.get_property_name()):t for t in cb.get_tracks() if isinstance(t,u.MovieSceneFloatTrack)}
    assert set(['CurrentFocalLength','CurrentAperture','ManualFocusDistance'])<=set(optics)
    if sh['label'] not in plans: continue
    p,t,fl,ap,focus_target=plans[sh['label']]; r=u.MathLibrary.find_look_at_rotation(u.Vector(*p),u.Vector(*t)); rot=[r.roll,r.pitch,r.yaw]
    values=dict(zip(['Location.X','Location.Y','Location.Z','Rotation.X','Rotation.Y','Rotation.Z'],p+rot)); assert set(values)<=set(ch)
    focus=norm(sub(focus_target,p)); assert focus>1
    for key,value in values.items(): changes.append((ch[key],value))
    for key,value in [('CurrentFocalLength',fl),('CurrentAperture',ap),('ManualFocusDistance',focus)]:
        channels=section_at(optics[key],sh).get_all_channels(); assert len(channels)==1; changes.append((channels[0],value))
    sh.update(position=p,rotation=rot,target=t,focal=fl,aperture=ap,focus=focus)
assert len(changes)==90
# Backup asset, then edit only existing sequence channels.
assert assets.duplicate_asset(DEST,BACKUP), 'Backup failed'
with u.ScopedEditorTransaction('Refine cinematic blocking 45s'):
    seq.modify()
    for channel,value in changes: channel.set_default(value)
    lib.open_level_sequence(seq)
    for sh in shots:
        lib.set_current_time((sh['start']+sh['end'])//2); lib.force_update()
        a=actors[sh['actor']]; c=a.get_cine_camera_component()
        assert norm(sub(xyz(a.get_actor_location()),sh['position']))<1, sh['label']+' transform mismatch'
        assert abs(c.current_focal_length-sh['focal'])<.1, sh['label']+' focal mismatch'
    assert assets.save_loaded_asset(seq)
(OUT/'shots_45s_refined.json').write_text(json.dumps(shots,indent=2),encoding='utf-8')
folder=OUT/'Refined'; folder.mkdir(exist_ok=True)
state={'i':0,'stage':0,'time':time.monotonic()}
def tick(dt):
    try:
        if time.monotonic()-state['time']<3: return
        i=state['i']
        if i==len(shots):
            u.unregister_slate_post_tick_callback(handle); lib.set_current_time(0); lib.force_update(); u.log('REFINED_11_CAPTURE_REQUESTS_COMPLETE'); return
        sh=shots[i]
        if state['stage']==0:
            lib.set_current_time((sh['start']+sh['end'])//2); lib.force_update(); state.update(stage=1,time=time.monotonic())
        else:
            u.AutomationLibrary.take_high_res_screenshot(1280,720,str(folder/(sh['label']+'.png')),camera=actors[sh['actor']]); state.update(i=i+1,stage=0,time=time.monotonic())
    except Exception as e:
        u.unregister_slate_post_tick_callback(handle); u.log_error(str(e))
handle=u.register_slate_post_tick_callback(tick)
u.log('REFINED_BLOCKING_45S_SAVED')
