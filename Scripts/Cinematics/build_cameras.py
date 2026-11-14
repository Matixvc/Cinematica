"""Interactive possessable blocking; writes only the new sequence, never the map.
Existing output is refused rather than overwritten. Close Sequencer to restore actors.
"""
import unreal as u
import math, json, time
from pathlib import Path

ROOT=Path(u.Paths.project_dir())
OUT=ROOT/'Saved/CinematicDirector'
DEST='/Game/Animacion/Cinematica/LS_Cameras_40s'
assert u.SystemLibrary.get_engine_version().startswith('5.6.1')
assert not u.EditorAssetLibrary.does_asset_exist(DEST), 'Sequence already exists; inspect it instead of duplicating or overwriting.'
assert (OUT/'possessable_test.json').exists(), 'Run test_possessable.py first'
u.LevelSequenceEditorBlueprintLibrary.close_level_sequence()
actors={a.get_actor_label():a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()}
assert '/Game/Animacion/Escenario/Escena.' in actors['Cam0'].get_path_name()
baseline={}
for name in ['Cam'+str(i) for i in range(9)]:
    a=actors[name]; c=a.get_cine_camera_component(); assert c
    baseline[name]={'transform':str(a.get_actor_transform()),'focal':c.current_focal_length,'aperture':c.current_aperture,'filmback':str(c.filmback),'focus':str(c.focus_settings)}
(OUT/'camera_baseline.json').write_text(json.dumps(baseline,indent=2),encoding='utf-8')
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
spec=[
 ('ESTABLISHING',0,96,24,cam0,mid,8),
 ('TWO_SHOT',96,216,35,camera(mid,780,40),mid,8),
 ('FATHER_REQUEST',216,312,50,camera(add(fh,mul(sub(head,fh),.20)),540,0),add(fh,mul(sub(head,fh),.20)),8),
 ('HAMMER_DETAIL',312,408,85,camera(mul(add(work,hammer),.5),360,90),mul(add(work,hammer),.5),8),
 ('FATHER_TENSION',408,528,50,camera(mul(add(fh,work),.5),420,-25),mul(add(fh,work),.5),8),
 ('HAMMER_TRACKING',528,600,35,camera(mid,780,30),mid,8),
 ('SON_REACTION',600,696,85,camera(head,330,0),head,5.6),
 ('RESOLUTION',696,840,35,camera(mid,780,45),mid,8),
 ('SON_POV',840,960,28,head,house,8),
]
seq=u.AssetToolsHelpers.get_asset_tools().create_asset('LS_Cameras_40s','/Game/Animacion/Cinematica',u.LevelSequence,u.LevelSequenceFactoryNew())
assert seq
u.EditorAssetLibrary.set_metadata_tag(seq,'CinematicDirectorOwner','unreal-cinematic-director-v1')
seq.set_display_rate(u.FrameRate(24,1)); seq.set_tick_resolution(u.FrameRate(24000,1))
seq.set_playback_start(0); seq.set_playback_end(960)
cuts=seq.add_track(u.MovieSceneCameraCutTrack)
u.LevelSequenceEditorBlueprintLibrary.open_level_sequence(seq)
shots=[]
def float_track(binding,name,path,value):
    tr=binding.add_track(u.MovieSceneFloatTrack)
    tr.set_property_name_and_path(name,path)
    sec=tr.add_section(); sec.set_range(0,960)
    sec.set_completion_mode(u.MovieSceneCompletionMode.RESTORE_STATE)
    sec.get_all_channels()[0].set_default(value)
    return sec
for i,(title,start,end,focal,pos,target,aperture) in enumerate(spec):
    actor=actors['Cam'+str(i)]
    binding=seq.add_possessable(actor)
    binding.set_name(f'CD_CAM_{i:02d}_{title}')
    c=actor.get_cine_camera_component(); assert c
    assert c.focus_settings.focus_method==u.CameraFocusMethod.MANUAL
    cb=seq.add_possessable(c); cb.set_parent(binding)
    cb.set_name(f'CD_OPTICS_{i:02d}')
    float_track(cb,'SensorWidth','Filmback.SensorWidth',36)
    float_track(cb,'SensorHeight','Filmback.SensorHeight',20.25)
    float_track(cb,'CurrentFocalLength','CurrentFocalLength',focal)
    float_track(cb,'CurrentAperture','CurrentAperture',aperture)
    float_track(cb,'ManualFocusDistance','FocusSettings.ManualFocusDistance',norm(sub(target,pos)))
    rotation=look(pos,target)
    for old_track in binding.get_tracks():
        if isinstance(old_track,u.MovieScene3DTransformTrack): binding.remove_track(old_track)
    track=binding.add_track(u.MovieScene3DTransformTrack); section=track.add_section(); section.set_range(0,960)
    section.set_completion_mode(u.MovieSceneCompletionMode.RESTORE_STATE)
    channels={str(ch.channel_name):ch for ch in section.get_all_channels()}
    scale=actor.get_actor_scale3d()
    values=dict(zip(['Location.X','Location.Y','Location.Z','Rotation.X','Rotation.Y','Rotation.Z','Scale.X','Scale.Y','Scale.Z'],pos+rotation+[scale.x,scale.y,scale.z]))
    assert set(values)<=set(channels), str(channels)
    for name,value in values.items(): channels[name].set_default(value)
    cut=cuts.add_section(); cut.set_range(start,end)
    bid=u.MovieSceneObjectBindingID(); bid.set_editor_property('guid',binding.get_id()); cut.set_camera_binding_id(bid)
    shots.append(dict(index=i,actor=actor.get_path_name(),title=title,start=start,end=end,focal=focal,aperture=aperture,position=pos,rotation=rotation,target=target,focus=norm(sub(target,pos))))
assert len(cuts.get_sections())==9 and len([b for b in seq.get_bindings() if b.get_name().startswith('CD_CAM_')])==9
assert u.EditorAssetLibrary.save_loaded_asset(seq)
(OUT/'shots.json').write_text(json.dumps(shots,indent=2),encoding='utf-8')
u.LevelSequenceEditorBlueprintLibrary.open_level_sequence(seq)
u.LevelSequenceEditorBlueprintLibrary.set_current_time(0)
u.log('CINEMATIC_STATIC_BLOCKING_SAVED')
# Capture static blocking through actual Sequencer evaluation, one request per settled frame.
_state={'i':0,'time':time.monotonic(),'stage':0}
def tick(dt):
    try:
        now=time.monotonic()
        if now-_state['time']<3: return
        i=_state['i']
        if i>=len(shots):
            u.unregister_slate_post_tick_callback(_handle)
            (OUT/'static_capture_complete.txt').write_text('9 capture requests completed; inspect image files.',encoding='utf-8')
            return
        if _state['stage']==0:
            u.LevelSequenceEditorBlueprintLibrary.set_current_time(shots[i]['start'])
            _state.update(stage=1,time=now)
        else:
            bid=cuts.get_sections()[i].get_camera_binding_id()
            bound=u.LevelSequenceEditorBlueprintLibrary.get_bound_objects(bid)
            assert len(bound)==1 and bound[0]==actors['Cam'+str(i)], 'Cut binding mismatch'
            c=bound[0].get_cine_camera_component()
            assert abs(c.current_focal_length-shots[i]['focal'])<.01
            assert abs(c.filmback.sensor_width-36)<.01, 'Filmback track not evaluated'
            u.AutomationLibrary.take_high_res_screenshot(1280,720,str(OUT/f'static_{i:02d}.png'),camera=bound[0])
            _state.update(i=i+1,stage=0,time=now)
    except Exception as exc:
        (OUT/'capture_error.txt').write_text(str(exc),encoding='utf-8')
        u.unregister_slate_post_tick_callback(_handle)
        raise
_handle=u.register_slate_post_tick_callback(tick)
