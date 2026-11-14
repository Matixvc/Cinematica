"""UNEXECUTED draft: animate only the owned sequence after static visual review.
The prerequisite sequence was not saved because build_cameras.py is blocked.
Rack focus and runtime validation remain pending.
"""
import unreal as u
import json, math, shutil, time
from pathlib import Path
ROOT=Path(u.Paths.project_dir()); OUT=ROOT/'Saved/CinematicDirector'
seq=u.load_asset('/Game/Animacion/Cinematica/LS_Cameras_40s')
assert seq and u.EditorAssetLibrary.get_metadata_tag(seq,'CinematicDirectorOwner')=='unreal-cinematic-director-v1'
assert (OUT/'blocking_reviewed.txt').exists(), 'Inspect the nine static previews before animation.'
backup=OUT/'LS_Cameras_40s_before_animation.uasset'
if not backup.exists(): shutil.copy2(ROOT/'Content/Animacion/Cinematica/LS_Cameras_40s.uasset',backup)
shots=json.loads((OUT/'shots.json').read_text(encoding='utf-8'))
def sub(a,b): return [x-y for x,y in zip(a,b)]
def add(a,b): return [x+y for x,y in zip(a,b)]
def mul(a,k): return [x*k for x in a]
def unit(v): return mul(v,1/math.sqrt(sum(x*x for x in v)))
def rot(p,t):
 r=u.MathLibrary.find_look_at_rotation(u.Vector(*p),u.Vector(*t)); return [r.roll,r.pitch,r.yaw]
bindings={b.get_name():b for b in seq.get_bindings() if b.get_name().startswith('CD_CAM_')}
for sh in shots:
 i=sh['index']; p=sh['position']; t=sh['target']; r=sh['rotation']
 b=bindings[f"CD_CAM_{i:02d}_{sh['title']}"]
 section=next(tr for tr in b.get_tracks() if isinstance(tr,u.MovieScene3DTransformTrack)).get_sections()[0]
 channels={str(c.channel_name):c for c in section.get_all_channels()}
 for c in channels.values():
  for k in c.get_keys(): c.remove_key(k)
 forward=unit(sub(t,p)); right=[-forward[1],forward[0],0]
 poses=[(sh['start'],p,r),(sh['end']-1,p,r)]
 if i in (0,4,7):
  end=add(p,mul(forward,{0:30,4:18,7:-35}[i])); poses[-1]=(sh['end']-1,end,rot(end,t))
 elif i==1:
  end=add(p,mul(right,25)); poses[-1]=(sh['end']-1,end,rot(end,t))
 elif i==5:
  data=json.loads((OUT/'inspection.json').read_text())
  aa={a['label']:a for a in data['actors']}
  a=aa['SM_Hammer']['center']; z=aa['SM_Hammer3']['center']
  poses=[(sh['start'],p,rot(p,a)),(sh['end']-1,p,rot(p,z))]
 elif i==8:
  data=json.loads((OUT/'inspection.json').read_text()); aa={a['label']:a for a in data['actors']}
  down=aa['SM_Hammer3']['center']; end=add(p,mul(forward,12))
  poses=[(840,p,r),(864,p,rot(p,down)),(900,p,rot(p,down)),(936,end,rot(end,t)),(959,end,rot(end,t))]
 names=['Location.X','Location.Y','Location.Z','Rotation.X','Rotation.Y','Rotation.Z','Scale.X','Scale.Y','Scale.Z']
 for frame,pos,rotation in poses:
  for name,val in zip(names,pos+rotation+[1,1,1]):
   channels[name].add_key(u.FrameNumber(frame),val,time_unit=u.MovieSceneTimeUnit.DISPLAY_RATE,interpolation=u.MovieSceneKeyInterpolation.AUTO)
 sh['poses']=[dict(frame=fr,position=pos,rotation=rr) for fr,pos,rr in poses]
assert u.EditorAssetLibrary.save_loaded_asset(seq)
(OUT/'animated_shots.json').write_text(json.dumps(shots,indent=2),encoding='utf-8')
u.LevelSequenceEditorBlueprintLibrary.open_level_sequence(seq)
u.LevelSequenceEditorBlueprintLibrary.set_current_time(0)
u.log('CINEMATIC_ANIMATION_SAVED')
