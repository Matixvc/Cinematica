"""Read-only Unreal Editor inspection; writes only a JSON report under Saved."""
import json
from pathlib import Path
import unreal as u

out = Path(u.Paths.project_dir()) / 'Saved/CinematicDirector'
out.mkdir(parents=True, exist_ok=True)
report = {'version': u.SystemLibrary.get_engine_version(), 'actors': [], 'bindings': [], 'apis': {}}
def vec(v):
    return [v.x, v.y, v.z]
level = u.get_editor_subsystem(u.LevelEditorSubsystem)
assert level.load_level('/Game/Animacion/Escenario/Escena')
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    origin, ext = a.get_actor_bounds(False)
    r = a.get_actor_rotation()
    row = dict(label=a.get_actor_label(), path=a.get_path_name(), cls=a.get_class().get_name(), location=vec(a.get_actor_location()), rotation=[r.pitch,r.yaw,r.roll], scale=vec(a.get_actor_scale3d()), center=vec(origin), extent=vec(ext))
    if isinstance(a, u.CineCameraActor):
        c=a.get_cine_camera_component()
        row['camera']=dict(focal=c.current_focal_length, aperture=c.current_aperture, filmback=str(c.filmback), focus=str(c.focus_settings))
    report['actors'].append(row)
s=u.load_asset('/Game/Animacion/Cinematica/LS_Cinematica_Final')
report['rate']=[s.get_display_rate().numerator,s.get_display_rate().denominator]
report['ticks']=[s.get_tick_resolution().numerator,s.get_tick_resolution().denominator]
report['range']=[s.get_playback_start(),s.get_playback_end()]
for b in s.get_bindings():
    report['bindings'].append(dict(name=b.get_name(), id=str(b.get_id()), tracks=[str(t.get_class().get_name()) for t in b.get_tracks()], template=str(b.get_object_template())))
report['root_tracks']=[str(t.get_class().get_name()) for t in s.get_tracks()]
for cls, methods in {'LevelSequenceEditorSubsystem':['add_spawnable_from_class','add_spawnable_from_instance'], 'MovieSceneSequenceExtensions':['add_possessable','make_binding_id'], 'MovieSceneBindingProxy':['get_object_template'], 'MovieSceneSectionExtensions':['get_channels'], 'MovieSceneScriptingDoubleChannel':['add_key'], 'MaterialEditingLibrary':['set_material_usage','recompile_material'], 'EditorAssetLibrary':['duplicate_asset','save_loaded_asset'], 'LevelSequenceEditorBlueprintLibrary':['set_current_time','get_bound_objects']}.items():
    obj=getattr(u,cls,None)
    report['apis'][cls]={m:getattr(getattr(obj,m,None),'__doc__',None) for m in methods}
mat=u.load_asset('/Game/Animacion/Recursos/MaterialInstanceConstant/rock_a066b5da7c')
report['rock']=str(mat)
report['material_chain']=[]
while mat:
    report['material_chain'].append(mat.get_path_name())
    if isinstance(mat,u.Material): break
    mat=mat.get_editor_property('parent')
(out/'inspection.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
u.log('CINEMATIC_INSPECTION_COMPLETE')
