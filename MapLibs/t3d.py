from pathlib import Path
import re

coord = r'((\+|-)\d+\.\d+)'
poly = re.compile(r'^(\s*Vertex\s+)'+coord+','+coord+','+coord+r'(\s*$)')

coord = r'(-?\d+(\.\d+)?)'
loc = re.compile(r'^(\s+\w+)=\((X=' + coord + ')?,?(Y=' + coord + ')?,?(Z=' + coord + ')?\)(\s*)$')

def MirrorList(l):
    # ensure proper vertex order
    return l[0:1] + l[-1:0:-1]

def FormatPolyCoord(f):
    posi = f >= 0
    f = abs(f)
    i = int(f)
    f -= i
    s = '+' if posi else '-'
    s += '{:0=5d}'.format(i)
    s += '{:.6f}'.format(f)[1:]
    return s

class Actor:
    def __init__(self, line:str):
        self.lines = [line]
    
    def Read(self, file, mult_coords:tuple|None):
        try:
            self._Read(file, mult_coords)
        except Exception as e:
            print('Exception in Actor::Read')
            print(self)
            print(e)
            raise

    def __str__(self):
        return ''.join(self.lines)
    
    def _Read(self, file, mult_coords:tuple|None):
        line:str = file.readline()
        while line:
            stripped:str = line.strip()
            if (stripped.startswith('Location=')
                or stripped.startswith('BasePos=')
                or stripped.startswith('SavedPos=')
                or stripped.startswith('OldLocation=')
                or stripped.startswith('PrePivot=')
                or stripped.startswith('BasePos=')):
                if mult_coords:
                    match = loc.match(line)
                    x = match.group(3)
                    if not x:
                        x = 0
                    x = str(float(x) * mult_coords[0])
                    y = match.group(6)
                    if not y:
                        y = 0
                    y = str(float(y) * mult_coords[1])
                    z = match.group(9)
                    if not z:
                        z = 0
                    z = str(float(z) * mult_coords[2])
                    line = match.group(1) + '=(X=' + x + ',Y=' + y + ',Z= ' + z + ')' + match.group(11)
            elif (stripped.startswith('Rotation=')
                  or stripped.startswith('BaseRot=')
                  or stripped.startswith('SavedRot=')):
                pass# TODO
            elif stripped.startswith('Begin Brush '):
                self.ReadBrush(line, file, mult_coords)
                line:str = file.readline()
                continue# don't append again, but we need to read the next line, yuck
            elif stripped.startswith('Begin '):
                raise NotImplementedError('unknown property: ' + line + ', in actor: ' + self.lines[0])

            self.lines.append(line)
            if stripped == 'End Actor':
                return
            line:str = file.readline()
        
        raise RuntimeError('unexpected end of actor?')
    
    def ReadBrush(self, line:str, file, mult_coords) -> None:
        while line:
            stripped:str = line.strip()
            if stripped.startswith('Begin Polygon '):
                self.ReadPolygon(line, file, mult_coords)
            else:
                self.lines.append(line)
            
            if stripped == 'End Brush':
                return
            line:str = file.readline()
        
        raise RuntimeError('unexpected end of brush?')

    def ReadPolygon(self, line:str, file, mult_coords) -> None:
        start = None
        while line:
            #print('ReadPolygon', line)
            stripped:str = line.strip()

            if stripped.startswith('Vertex ') and mult_coords:
                if not start:
                    start = len(self.lines)-1
                match = poly.match(line)
                x = match.group(2)
                y = match.group(4)
                z = match.group(6)
                # does the import process care about the exact format and number of decimal places?
                x = float(x)*mult_coords[0]
                x = FormatPolyCoord(x)
                y = float(y)*mult_coords[1]
                y = FormatPolyCoord(y)
                z = float(z)*mult_coords[2]
                z = FormatPolyCoord(z)
                line = match.group(1) + x +',' + y +',' + z + match.group(8)

            self.lines.append(line)
            if stripped == 'End Polygon':
                if mult_coords:
                    # assert we finished with at least 3 vertices, and mirror the list
                    end = len(self.lines)-2
                    #print('\nEnd Polygon', start, end)
                    #print(self.lines[start:end])
                    assert self.lines[end].strip().startswith('Vertex ')
                    assert end-start >= 2
                    self.lines[start:end] = MirrorList(self.lines[start:end])
                    #print(self.lines[start:end])
                return

            line:str = file.readline()
        
        raise RuntimeError('unexpected end of polygon?')

class Map:
    def __init__(self):
        self.actors = []
        self.mult_coords = None#(1,1,1)

    def SetMirror(self, mult_coords:tuple):
        assert len(mult_coords) == 3
        self.mult_coords = mult_coords
    
    def Read(self, filepath:Path):
        with open(filepath, 'r') as file:
            self._Read(file)

    def _Read(self, file):
        line = file.readline().strip()
        assert line == 'Begin Map'
        line = file.readline()
        while line:
            stripped = line.strip()
            if stripped.startswith('Begin Actor '):
                actor = Actor(line)
                actor.Read(file, self.mult_coords)
                self.actors.append(actor)
            elif stripped == 'End Map':
                break
            else:
                raise NotImplementedError('unknown type', line)
            line = file.readline()
        
        print('finished reading map,', len(self.actors), 'actors')
    
    def Write(self, outpath:Path):
        with open(outpath, 'w', newline='\r\n') as f:
            f.write('Begin Map\n')
            for a in self.actors:
                f.write(str(a))
            f.write('End Map\n')

