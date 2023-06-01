from pathlib import Path
import re

coord = r'((\+|-)\d+\.\d+)'
poly = re.compile(r'^(\s*Vertex\s+)'+coord+','+coord+','+coord+r'(\s*$)')

coord = r'(-?\d+(\.\d+)?)'
vect_pattern = r'\((X=' + coord + ')?,?(Y=' + coord + ')?,?(Z=' + coord + ')?\)'
vect_regex = re.compile(vect_pattern)
loc = re.compile(r'^(\s+\w+)=' + vect_pattern + r'(\s*)$')

axis = r'(-?\d+)'
rot = re.compile(r'^(\s+[^=]+)=\((Pitch=' +axis+ r')?,?(Yaw=' +axis+ r')?,?(Roll=' +axis+ r')?\)(\s*)$')

getclassname = re.compile(r'^Begin Actor Class=([^ ]+) Name=([^ ]+)\s*$')

prop_regex = re.compile(r'^\s*([^=]+)=.*$')

scale_regex = re.compile(r'^([^=]+)=\((Scale=' + vect_pattern + r',)?(.*\))(\s*)$')

# some models like the pinball machine are sideways, so the math doesn't match the appearance
classes_rot_offsets = dict(
    Pinball=32768,
    Chair1=32768,
    Brush=0,
)

def MirrorList(l):
    # ensure proper vertex order
    return l[0:1] + l[-1:0:-1]

def mirror_rotation(r, offset):
    yaw = int(r[1])
    yaw %= 65535 # 65535 is more accurate than 65536, I guess it's true that 65535 is 360 degrees and not 65536
    yaw += offset # offset by 16384 because we want to align with north/south not west/east, if this was a clock we want yaw 0 to be 12 o'clock
    yaw = -yaw
    yaw -= offset # undo the offset
    yaw %= 65535
    return (r[0], yaw, r[2])

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
        match = getclassname.match(line)
        self.classname = match.group(1)
        self.objectname = match.group(2)
        self.polylist = None
        self.props = dict()
    
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
    
    def IsBrush(self) -> bool:
        return self.classname in ['Brush', 'Mover', 'DeusExMover', 'BreakableGlass', 'ElevatorMover', 'MultiMover']

    def IsMover(self) -> bool:
        return self.classname in ['Mover', 'DeusExMover', 'BreakableGlass', 'ElevatorMover', 'MultiMover']

    def Finalize(self):# TODO: more checks in finalize
        if self.classname=='Brush':
            assert self.polylist
        else:
            assert not self.polylist
        if self.IsMover() and 'PostScale' not in self.props:
            line = '    PostScale=(Scale=(X={},Y={},Z={}),SheerAxis=SHEER_ZX)\n'.format(-1,1,1)
            self.lines.insert(-1, line)
            self.props['PostScale'] = line
            raise NotImplementedError('TODO: missing PostScale in Finalize')
    
    def ProcLoc(self, line:str, mult_coords:tuple|None) -> str:
        if not mult_coords:
            return line
        match = loc.match(line)

        x = match.group(3)
        if not x:
            x = 0
        x = float(x) * mult_coords[0]

        y = match.group(6)
        if not y:
            y = 0
        y = float(y) * mult_coords[1]

        z = match.group(9)
        if not z:
            z = 0
        z = float(z) * mult_coords[2]

        line = match.group(1) + '=(X={},Y={},Z={})'.format(x,y,z) + match.group(11)
        return line
    
    def ProcRot(self, line:str, mult_coords:tuple|None) -> str:
        if not mult_coords:
            return line
        match = rot.match(line)

        pitch = match.group(3)
        if not pitch:
            pitch = 0

        yaw = match.group(5)
        if not yaw:
            yaw = 0

        roll = match.group(7)
        if not roll:
            roll = 0

        # TODO: this is only correct when mirroring X
        classname = self.classname
        if self.IsBrush():
            classname = 'Brush'
        rot_offset = classes_rot_offsets.get(classname, 16384)
        (pitch, yaw, roll) = mirror_rotation((pitch,yaw,roll), rot_offset)
        line = match.group(1) + '=(Pitch={},Yaw={},Roll={})'.format(pitch,yaw,roll) + match.group(8)
        return line
    
    def FixMoverPostScale(self, line:str, mult_coords) -> str:
        m = scale_regex.match(line)
        x = m.group(4)
        if not x:
            x=1
        y = m.group(7)
        if not y:
            y=1
        z = m.group(10)
        if not z:
            z=1
        x = float(x) * mult_coords[0]
        y = float(y) * mult_coords[1]
        z = float(z) * mult_coords[2]
        line = m.group(1) + '=(Scale=' + '(X={},Y={},Z={})'.format(x,y,z) + ',' + m.group(12) + m.group(13)
        return line
    
    def _Read(self, file, mult_coords:tuple|None):
        # TODO: save rotation, location, prepivot, and polylist?
        line:str = file.readline()
        while line:
            stripped:str = line.strip()
            prop = prop_regex.match(stripped)
            if prop:
                self.props[prop.group(1)] = line
            
            if (stripped.startswith('Location=')
                or stripped.startswith('BasePos=')
                or stripped.startswith('SavedPos=')
                or stripped.startswith('OldLocation=')
                or (stripped.startswith('PrePivot=') and not self.IsMover())
                or stripped.startswith('BasePos=')):
                # parse and multiply
                line = self.ProcLoc(line, mult_coords)

            elif not self.IsMover() and (stripped.startswith('Rotation=')
                  or stripped.startswith('BaseRot=')
                  or stripped.startswith('SavedRot=')
                  or stripped.startswith('KeyRot')
                  or stripped.startswith('ViewRotation')):
                # parse and fix
                line = self.ProcRot(line, mult_coords)
            elif stripped.startswith('PostScale') and self.IsMover():
                line = self.FixMoverPostScale(line, mult_coords)

            elif stripped.startswith('Begin Brush '):
                self.ReadBrush(line, file, mult_coords)
                line:str = file.readline()
                continue# HACK: don't append again, but we need to read the next line, yuck
            elif stripped.startswith('Begin '):
                raise NotImplementedError('unknown property: ' + line + ', in actor: ' + self.lines[0])

            self.lines.append(line)
            if stripped == 'End Actor':
                self.Finalize()
                return
            line:str = file.readline()
        
        raise RuntimeError('unexpected end of actor?')
    
    def ReadBrush(self, line:str, file, mult_coords) -> None:
        if not self.IsBrush():
            raise RuntimeError('unexpected Brush in class '+self.classname)
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

    def AdjustVert(self, line:str, mult_coords) -> str:
        # TODO: convert coords to world space, perform mirror, then convert back to object space for saving
        if not mult_coords:
            return line
        match = poly.match(line)
        x = float(match.group(2))
        y = float(match.group(4))
        z = float(match.group(6))

        x *= mult_coords[0]
        x = FormatPolyCoord(x)
        y *= mult_coords[1]
        y = FormatPolyCoord(y)
        z *= mult_coords[2]
        z = FormatPolyCoord(z)

        line = match.group(1) + '{},{},{}'.format(x,y,z) + match.group(8)
        return line
    
    def ReadPolygon(self, line:str, file, mult_coords) -> None:
        start = None
        while line:
            #print('ReadPolygon', line)
            stripped:str = line.strip()

            # Movers use PostScale instead of modifying vertices
            if stripped.startswith('Vertex ') and not self.IsMover():
                if not start:
                    start = len(self.lines)-1
                line = self.AdjustVert(line, mult_coords)

            self.lines.append(line)
            if stripped == 'End Polygon':
                if self.IsMover():
                    return
                # assert we finished with at least 3 vertices
                end = len(self.lines)-2
                #print('\nEnd Polygon', start, end)
                #print(self.lines[start:end])
                assert self.lines[end].strip().startswith('Vertex ')
                assert end-start >= 2
                if mult_coords:
                    self.lines[start:end] = MirrorList(self.lines[start:end])
                    #print(self.lines[start:end])
                self.polylist = [*range(start, end)]
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

