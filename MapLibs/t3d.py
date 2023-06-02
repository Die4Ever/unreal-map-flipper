from pathlib import Path
from MapLibs.actor import CreateActor

def GetDefaultOut() -> Path:
    root = Path(__file__).resolve().parent.parent
    assert root.is_dir()
    assert (root / 'mirror.py').exists()
    p = root / 'out'
    p.mkdir(exist_ok=True)
    return p


class Map:
    def __init__(self):
        self.actors = []
        self.mult_coords = None#(1,1,1)
        self.name = None

    def SetMirror(self, mult_coords:tuple):
        assert len(mult_coords) == 3
        self.mult_coords = mult_coords
    
    def Read(self, filepath:Path):
        self.SetMapName(filepath.name)
        with open(filepath, 'r') as file:
            self._Read(file)

    def _Read(self, file):
        line = file.readline().strip()
        assert line == 'Begin Map'
        line = file.readline()
        while line:
            stripped = line.strip()
            if stripped.startswith('Begin Actor '):
                actor = CreateActor(self, line)
                actor.Read(file, self.mult_coords)
                self.actors.append(actor)
            elif stripped == 'End Map':
                break
            else:
                raise NotImplementedError('unknown type', line)
            line = file.readline()
        
        print('finished reading map', self.name, len(self.actors), 'actors')
    

    def SetMapName(self, name:str):
        # strip the quotes and whitespace
        name = name.strip().replace('"', '')
        if name:
            self.name = name
    

    def Write(self, outpath:Path):
        if outpath.is_dir() and self.name:
            name = self.name
            if self.mult_coords:
                m = self.mult_coords
                name += '_{}_{}_{}'.format(m[0], m[1], m[2])
            name += '.t3d'
            outpath = outpath / name
        
        with open(outpath, 'w', newline='\r\n') as f:
            f.write('Begin Map\n')
            for a in self.actors:
                f.write(str(a))
            f.write('End Map\n')
        print('wrote out to', outpath)

