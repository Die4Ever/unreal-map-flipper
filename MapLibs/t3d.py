from collections import OrderedDict
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
        self.actors = OrderedDict()
        self.mult_coords = None#(1,1,1)
        self.name = None

    def SetMirror(self, mult_coords:tuple):
        assert len(mult_coords) == 3
        self.mult_coords = mult_coords
    
    def Read(self, filepath:Path):
        print('reading', filepath)
        self.SetMapName(filepath.name)
        with open(filepath, 'r') as file:
            self._Read(file)

        self.before_finalize()
        for a in self.actors.values():
            a.Finalize(self.mult_coords)
        self.after_finalize()

    def RemoveActor(self, name:str) -> bool:
        if name not in self.actors:
            print('failed to remove actor', name)
            return False
        self.actors.pop(name)
        return True

    def before_finalize(self):
        #if self.name in ('02_NYC_Hotel', '04_NYC_Hotel', '08_NYC_Hotel'):
            # needs a lot of work lol
            # brush = self.actors.get('DeusExMover3')
            # if brush:
            #     brush.useMirrorVerts = True
            # brush = self.actors.get('DeusExMover4')
            # if brush:
            #     brush.useMirrorVerts = True

        if self.name == '02_NYC_Warehouse':
            # remove the stupid fence parts that aren't breakable
            self.RemoveActor('Brush407')
            self.RemoveActor('Brush391')
            self.RemoveActor('Brush389')
            self.RemoveActor('Brush392')
            self.RemoveActor('Brush396')
            self.RemoveActor('Brush395')
            self.RemoveActor('Brush390')

        elif self.name == '03_NYC_Airfield':
            brush = self.actors.get('Brush738')
            if brush:
                brush.RemovePolyFlag(5)
        
        elif self.name == '03_NYC_BatteryPark':
            brush = self.actors.get('DeusExMover2')
            if brush:
                brush.useMirrorVerts = True

        elif self.name == '12_Vandenburg_Cmd':
            brush = self.actors.get('Brush341')
            if brush:
                brush.RemovePolyFlag(5)

        elif self.name == '15_Area51_Bunker':
            brush = self.actors.get('Brush386')
            if brush:
                brush.RemovePolyFlag(7, polys=[1])

    def after_finalize(self):
        pass


    def _Read(self, file):
        line = file.readline().strip()
        assert line == 'Begin Map'
        line = file.readline()
        while line:
            stripped = line.strip()
            if stripped.startswith('Begin Actor '):
                actor = CreateActor(self, line)
                actor.Read(file, self.mult_coords)
                if actor.objectname not in self.actors:
                    self.actors[actor.objectname] = actor
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
    
    def ToString(self):
        s = 'Begin Map\n'
        for a in self.actors.values():
            s += str(a)
        s += 'End Map\n'
        return s

    def Write(self, outpath:Path):
        if outpath.is_dir() and self.name:
            name = self.name
            if self.mult_coords:
                m = self.mult_coords
                name += '_{}_{}_{}'.format(m[0], m[1], m[2])
            name += '.t3d'
            outpath = outpath / name
        
        with open(outpath, 'w', newline='\r\n') as f:
            f.write(self.ToString())
        print('wrote out to', outpath)

