from pathlib import Path
from MapLibs.t3d import Map, GetDefaultOut

# TODO: find or make our own map to upload as test data without copyright issues?
m = Map()
m.SetMirror((-1,1,1))
m.Read(Path('C:/temp/barlevel.t3d'))
m.Write(GetDefaultOut() / 'mirroredbar.t3d')

m = Map()
m.SetMirror((-1,1,1))
m.Read(Path('C:/temp/airfield.t3d'))
m.Write(GetDefaultOut() / 'mirroredairfield.t3d')
