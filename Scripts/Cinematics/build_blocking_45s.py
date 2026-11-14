"""Interactive possessable blocking; writes only the new sequence, never the map.
Existing output is refused rather than overwritten. Close Sequencer to restore actors.
"""
import unreal as u
import math, json, time
from pathlib import Path

ROOT=Path(u.Paths.project_dir())
OUT=ROOT/'Saved/CinematicDirector'
DEST='/Game/Animacion/Cinematica/LS_Cameras_45s'
assert u.SystemLibrary.get_engine_version().startswith('5.6.1')
assert not u.EditorAssetLibrary.does_asset_exist(DEST), 'Sequence already exists; inspect it instead of duplicating or overwriting.'
assert (OUT/'possessable_test.json').exists(), 'Run test_possessable.py first'
u.LevelSequenceEditorBlueprintLibrary.close_level_sequence()
actors={a.get_actor_label():a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()}
assert '/Game/Animacion/Escenario/Escena.' in actors['Cam0'].get_path_name()
OUT.mkdir(parents=True,exist_ok=True)
baseline={}
for name in ['Cam'+str(i) for i in range(9)]:
    a=actors[name]; c=a.get_cine_camera_component(); assert c
    baseline[name]={'transform':str(a.get_actor_transform()),'focal':c.current_focal_length,'aperture':c.current_aperture,'filmback':str(c.filmback),'focus':str(c.focus_settings)}
(OUT/'camera_baseline_45s.json').write_text(json.dumps(baseline,indent=2),encoding='utf-8')
def xyz(v): return [v.x,v.y,v.z]
def add(a,b): return [x+y for x,y in zip(a,b)]
def sub(a,b): return [x-y for x,y in zip(a,b)]
def mul(a,k): return [x*k for x in a]
def norm(a): return math.sqrt(sum(x*x for x in a))
def unit(a): return mul(a,1/norm(a))
def center(name): return xyz(actors[name].get_actor_bounds(False)[0])
def loc(name): return xyz(actors[name].get_actor_location())
def look(p,t):
    r=u.MathLibrary.find_look_at_rotation(u.Vector(*p),u.Vector(*t))
    return [r.roll,r.pitch,r.yaw]
f=loc('BP_Father_ThirdPersonCharacter'); s=loc('BP_Son_ThirdPersonCharacter')
house=center('DogHouse_Base'); work=center('Lista_Madera_02_DogHouse'); hammer=center('SM_Hammer')
head=center('Auriculares'); head[2]-=4
fh=[f[0],f[1],f[2]+65]
mid=mul(add(f,s),.5); mid[2]=100
cam0=loc('Cam0'); front=unit([cam0[0]-mid[0],cam0[1]-mid[1],0])
right=[front[1],-front[0],0]
def camera(target,distance,height=0): return add(add(target,mul(front,distance)),[0,0,height])
# Initial blocking, based on live actor locations. Distances in cm.
crate=center('WoodenCrate2'); impact=center('SM_Hammer3')
# Use the ground beside the crate, not the son's head, for the impact insert.
impact=[crate[0]-65,crate[1]+20,12]
def blend(a,b,t): return add(a,mul(sub(b,a),t))
def shotpos(t,d,h=0,side=0): return add(camera(t,d,h),mul(right,side))
worktarget=blend(fh,work,.55)
request=blend(fh,head,.35)
reaction=blend(head,fh,.25)
# A frontal angle keeps father screen-left and son screen-right.
spec=[
 ('CAM00','ESTABLISHING',0,72,26,shotpos(mid,1050,180),mid,8,'Cam0'),
 ('CAM01','PRESENTATION',72,192,35,shotpos(mid,650,35),mid,5.6,'Cam1'),
 ('CAM02','FATHER_REQUEST',192,288,50,shotpos(request,650,15,-130),request,2.8,'Cam2'),
 ('CAM03','FATHER_FRUSTRATED',288,432,40,shotpos(worktarget,650,45,-100),worktarget,5.6,'Cam3'),
 ('CAM03_1','BOARD_DETAIL',432,456,85,shotpos(work,160,55,-35),work,4,'Cam0'),
 ('CAM04','FATHER_TENSION',456,600,40,shotpos(worktarget,620,25,-65),worktarget,5.6,'Cam4'),
 ('CAM05','HAMMER_LAUNCH',600,672,35,shotpos(mid,720,25,40),mid,8,'Cam5'),
 ('CAM05_1','HAMMER_IMPACT',672,696,70,shotpos(impact,180,65,35),impact,5.6,'Cam0'),
 ('CAM06','SON_REACTION',696,792,50,shotpos(reaction,620,10,100),reaction,5.6,'Cam6'),
 ('CAM07','RESOLUTION',792,936,40,shotpos(mid,690,65,-40),mid,8,'Cam7'),
 ('CAM08','SON_POV',936,1080,28,add(head,[0,0,0]),blend(house,fh,.20),8,'Cam8'),
]
assert len(spec)==11 and spec[0][2]==0 and spec[-1][3]==1080
assert all(a[3]==b[2] for a,b in zip(spec,spec[1:]))
assert all(norm(sub(p,t))>1 for _,_,_,_,_,p,t,_,_ in spec)
for name in {x[-1] for x in spec}:
    assert actors[name].get_cine_camera_component().focus_settings.focus_method==u.CameraFocusMethod.MANUAL, name+' requires manual focus'
seq=u.AssetToolsHelpers.get_asset_tools().create_asset('LS_Cameras_45s','/Game/Animacion/Cinematica',u.LevelSequence,u.LevelSequenceFactoryNew())
assert seq
u.EditorAssetLibrary.set_metadata_tag(seq,'CinematicDirectorOwner','blocking-45s-v1')
seq.set_display_rate(u.FrameRate(24,1)); seq.set_tick_resolution(u.FrameRate(24000,1))
seq.set_playback_start(0); seq.set_playback_end(1080)
cuts=seq.add_track(u.MovieSceneCameraCutTrack)
lib=u.LevelSequenceEditorBlueprintLibrary
lib.open_level_sequence(seq)
tracks={}; shots=[]
props=[('SensorWidth','Filmback.SensorWidth'),('SensorHeight','Filmback.SensorHeight'),('CurrentFocalLength','CurrentFocalLength'),('CurrentAperture','CurrentAperture'),('ManualFocusDistance','FocusSettings.ManualFocusDistance')]
for label,title,start,end,focal,pos,target,aperture,name in spec:
    actor=actors[name]
    if name not in tracks:
        binding=seq.add_possessable(actor); binding.set_name('CD_CAM_'+name)
        cb=seq.add_possessable(actor.get_cine_camera_component()); cb.set_parent(binding); cb.set_name('CD_OPTICS_'+name)
        tr=binding.add_track(u.MovieScene3DTransformTrack)
        optics=[]
        for prop,path in props:
            ot=cb.add_track(u.MovieSceneFloatTrack); ot.set_property_name_and_path(prop,path); optics.append(ot)
        tracks[name]=(binding,tr,optics)
    binding,tr,optics=tracks[name]
    def section(track):
        sec=track.add_section(); sec.set_range(start,end); sec.set_completion_mode(u.MovieSceneCompletionMode.RESTORE_STATE); return sec
    focus=norm(sub(target,pos)); rotation=look(pos,target)
    for ot,value in zip(optics,[36,20.25,focal,aperture,focus]):
        section(ot).get_all_channels()[0].set_default(value)
    sec=section(tr); channels={str(ch.channel_name):ch for ch in sec.get_all_channels()}
    scale=actor.get_actor_scale3d()
    values=dict(zip(['Location.X','Location.Y','Location.Z','Rotation.X','Rotation.Y','Rotation.Z','Scale.X','Scale.Y','Scale.Z'],pos+rotation+[scale.x,scale.y,scale.z]))
    assert set(values)<=set(channels),str(channels)
    for key,value in values.items(): channels[key].set_default(value)
    cut=cuts.add_section(); cut.set_range(start,end)
    bid=u.MovieSceneObjectBindingID(); bid.set_editor_property('guid',binding.get_id()); cut.set_camera_binding_id(bid)
    shots.append(dict(label=label,title=title,actor=name,start=start,end=end,position=pos,rotation=rotation,target=target,focal=focal,aperture=aperture,focus=focus))
assert len(cuts.get_sections())==11 and len(tracks)==9
# Verify actual evaluated bindings and transforms at the middle of each cut.
for shot in shots:
    lib.set_current_time((shot['start']+shot['end'])//2); lib.force_update()
    actor=actors[shot['actor']]; binding=tracks[shot['actor']][0]
    bid=u.MovieSceneObjectBindingID(); bid.set_editor_property('guid',binding.get_id())
    assert actor in lib.get_bound_objects(bid), shot['label']+' binding failed'
    assert norm(sub(xyz(actor.get_actor_location()),shot['position']))<1, shot['label']+' transform failed'
    assert abs(actor.get_cine_camera_component().current_focal_length-shot['focal'])<.1, shot['label']+' focal failed'
assert u.EditorAssetLibrary.save_loaded_asset(seq)
(OUT/'shots_45s.json').write_text(json.dumps(shots,indent=2),encoding='utf-8')
lib.set_current_time(0); lib.force_update()
u.log('CINEMATIC_BLOCKING_45S_SAVED')
# Optional screenshots: use actual evaluated cameras, one request per settled frame.
_state={'i':0,'time':time.monotonic(),'stage':0}
def tick(dt):
    try:
        now=time.monotonic()
        if now-_state['time']<3: return
        i=_state['i']
        if i>=len(shots):
            u.unregister_slate_post_tick_callback(_handle)
            lib.set_current_time(0)
            u.log('11 capture requests completed; inspect image files')
            return
        sh=shots[i]
        if _state['stage']==0:
            lib.set_current_time((sh['start']+sh['end'])//2); lib.force_update()
            _state.update(stage=1,time=now)
        else:
            u.AutomationLibrary.take_high_res_screenshot(1280,720,str(OUT/(sh['label']+'.png')),camera=actors[sh['actor']])
            _state.update(i=i+1,stage=0,time=now)
    except Exception as exc:
        (OUT/'capture_error_45s.txt').write_text(str(exc),encoding='utf-8')
        u.unregister_slate_post_tick_callback(_handle)
        u.log_warning(str(exc))
_handle=u.register_slate_post_tick_callback(tick)
