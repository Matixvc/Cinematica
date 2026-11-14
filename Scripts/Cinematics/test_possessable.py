"""Interactive Cam0 test. Never loads/saves a map or changes actor properties."""
import unreal as u
import json
from pathlib import Path

out=Path(u.Paths.project_dir())/'Saved/CinematicDirector'
out.mkdir(parents=True,exist_ok=True)
lib=u.LevelSequenceEditorBlueprintLibrary
lib.close_level_sequence()
actors=u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
matches=[a for a in actors if a.get_actor_label()=='Cam0']
assert len(matches)==1, 'Cam0 missing or ambiguous'
cam=matches[0]
assert isinstance(cam,u.CineCameraActor) and cam.get_cine_camera_component()
assert '/Game/Animacion/Escenario/Escena.' in cam.get_path_name()
path='/Game/Animacion/Cinematica/LS_Cam0_Possessable_Test'
if u.EditorAssetLibrary.does_asset_exist(path):
    seq=u.load_asset(path)
    assert u.EditorAssetLibrary.get_metadata_tag(seq,'CinematicDirectorOwner')=='possessable-test-v1'
else:
    seq=u.AssetToolsHelpers.get_asset_tools().create_asset('LS_Cam0_Possessable_Test','/Game/Animacion/Cinematica',u.LevelSequence,u.LevelSequenceFactoryNew())
    u.EditorAssetLibrary.set_metadata_tag(seq,'CinematicDirectorOwner','possessable-test-v1')
    seq.set_display_rate(u.FrameRate(24,1)); seq.set_tick_resolution(u.FrameRate(24000,1))
    seq.set_playback_start(0); seq.set_playback_end(96)
    binding=seq.add_possessable(cam); binding.set_name('TEST_Cam0')
    section=binding.add_track(u.MovieScene3DTransformTrack).add_section()
    section.set_range(0,96); section.set_completion_mode(u.MovieSceneCompletionMode.RESTORE_STATE)
    p=cam.get_actor_location(); r=cam.get_actor_rotation(); s=cam.get_actor_scale3d()
    vals=[p.x,p.y,p.z,r.roll,r.pitch,r.yaw,s.x,s.y,s.z]
    names=['Location.X','Location.Y','Location.Z','Rotation.X','Rotation.Y','Rotation.Z','Scale.X','Scale.Y','Scale.Z']
    channels={str(ch.channel_name):ch for ch in section.get_all_channels()}
    assert set(names)<=set(channels), str(channels)
    for name,val in zip(names,vals): channels[name].set_default(val)
    cut=seq.add_track(u.MovieSceneCameraCutTrack).add_section(); cut.set_range(0,96)
    bid=u.MovieSceneObjectBindingID(); bid.set_editor_property('guid',binding.get_id()); cut.set_camera_binding_id(bid)
assert lib.open_level_sequence(seq)
lib.set_current_time(0); lib.force_update()
binding=next(b for b in seq.get_bindings() if b.get_name()=='TEST_Cam0')
bid=u.MovieSceneObjectBindingID(); bid.set_editor_property('guid',binding.get_id())
resolved=lib.get_bound_objects(bid)
assert cam in resolved, 'Possessable binding did not resolve Cam0'
assert u.EditorAssetLibrary.save_loaded_asset(seq)
report={'status':'PASS_BINDING','sequence':path,'actor':cam.get_path_name(),'component':cam.get_cine_camera_component().get_path_name(),'resolved':[a.get_path_name() for a in resolved]}
(out/'possessable_test.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
u.AutomationLibrary.take_high_res_screenshot(1280,720,str(out/'test_cam0.png'),camera=cam,delay=2)
u.log('CINEMATIC_POSSESSABLE_TEST_PASS')
