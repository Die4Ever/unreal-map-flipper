from MapLibs.t3d import *
import re

coord = r'((\+|-)\d+\.\d+)'
poly = re.compile(r'^(\s*\w+\s+)'+coord+','+coord+','+coord+r'(\s*$)')

poly_prop = re.compile(r'^(\s*)(\w+)(\s+)(.*)$')

pan_regex = re.compile(r'^(\s+Pan\s+)U=([^\s]+)\s+V=([^\s]+)(\s*)$')

coord = r'(-?\d+(\.\d+)?)'
vect_pattern = r'\((X=' + coord + ')?,?(Y=' + coord + ')?,?(Z=' + coord + ')?\)'
vect_regex = re.compile(vect_pattern)
loc = re.compile(r'^(\s+\w+)=' + vect_pattern + r'(\s*)$')

axis = r'(-?\d+)'
rot = re.compile(r'^(\s+[^=]+)=\((Pitch=' +axis+ r')?,?(Yaw=' +axis+ r')?,?(Roll=' +axis+ r')?\)(\s*)$')

getclassname = re.compile(r'^Begin Actor Class=([^ ]+) Name=([^ ]+)\s*$')

prop_regex = re.compile(r'^(\s*)([^=]+)=(.*)$')

scale_regex = re.compile(r'^([^=]+)=\((Scale=' + vect_pattern + r',)?(.*\))(\s*)$')


# some models like the pinball machine are sideways, so the math doesn't match the appearance
# default is 16384 not 0, at least for ScriptedPawns
classes_rot_offsets = dict(
    Pinball=32768,
    Chair1=32768,
    Brush=0,
    CouchLeather=0,
    WaterCooler=0,
    Toilet=0,
    HangingChicken=0, # very important
)


# keep list of vertices counter-clockwise
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


# t3d files are really strict about the formatting of poly coords
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
    mover_classes = set(('Mover', 'DeusExMover', 'BreakableGlass', 'ElevatorMover', 'MultiMover', 'BreakableWall'))
    brush_classes = set(('Brush', *mover_classes))

    def __init__(self, line:str):
        self.lines = [line]
        match = getclassname.match(line)
        self.classname = match.group(1)
        self.objectname = match.group(2)
        self.polylist = []
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
        return False


    def IsMover(self) -> bool:
        return False


    def GetPropIdx(self, prop:str) -> int|None:
        return self.props.get(prop)
    
    def IterProps(self, *p) -> list:
        ret = []
        for prop in p:
            if prop in self.props:
                ret.append(self.GetPropIdx(prop))
        return ret


    def Finalize(self, mult_coords):# TODO: more checks in finalize
        if self.IsBrush():
            assert self.polylist
        else:
            assert not self.polylist

        for i in self.IterProps('Location', 'BasePos', 'SavedPos', 'OldLocation'):
            self.lines[i] = self.ProcLoc(self.lines[i], mult_coords)
        
        if not self.IsMover() and 'PrePivot' in self.props:
            i = self.GetPropIdx('PrePivot')
            self.lines[i] = self.ProcLoc(self.lines[i], mult_coords)

        if not self.IsMover():
            if not self.GetPropIdx('Rotation'):
                self.props['Rotation'] = len(self.lines)-2
                line = '    Rotation=(Pitch=0,Yaw=0,Roll=0)\n' # stick this default in so we can correct it below
                self.lines.insert(-2, line) # don't overwrite the End Actor

            for i in self.IterProps('Rotation', 'BaseRot', 'SavedRot', 'ViewRotation'):
                self.lines[i] = self.ProcRot(self.lines[i], mult_coords)
            
            for (prop, i) in self.props.items():
                if not prop.startswith('KeyRot('):
                    continue
                self.lines[i] = self.ProcRot(self.lines[i], mult_coords)
        #


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
        # temporary variable to get classes_rot_offsets, all Brushes are the same
        classname = self.classname
        if self.IsBrush():
            classname = 'Brush'
        rot_offset = classes_rot_offsets.get(classname, 16384)
        (pitch, yaw, roll) = mirror_rotation((pitch,yaw,roll), rot_offset)
        line = match.group(1) + '=(Pitch={},Yaw={},Roll={})'.format(pitch,yaw,roll) + match.group(8)
        return line
    

    def FixMoverPostScale(self, line:str, mult_coords) -> str:
        if not mult_coords:
            return line
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

            if stripped.startswith('Begin Brush '):
                stripped = '' # don't try to add this as a property
                line = self.ReadBrush(line, file, mult_coords)

            elif stripped.startswith('Begin '):
                raise NotImplementedError('unknown property: ' + line + ', in actor: ' + self.lines[0])

            prop = prop_regex.match(line)
            if prop: # TODO: should we save the prop.groups() list?
                self.props[prop.group(2)] = len(self.lines)
            self.lines.append(line)
            if stripped == 'End Actor':
                self.Finalize(mult_coords)
                return
            line:str = file.readline()
        
        raise RuntimeError('unexpected end of actor?')
    

    def ReadBrush(self, line:str, file, mult_coords) -> str:
        raise RuntimeError('unexpected Brush in class '+self.classname)


class Brush(Actor):
    def IsBrush(self) -> bool:
        return True
    
    def Finalize(self, mult_coords):# TODO: more checks in finalize
        super().Finalize(mult_coords)
        
    def ReadBrush(self, line:str, file, mult_coords) -> str:
        while line:
            stripped:str = line.strip()
            if stripped.startswith('Begin Polygon '):
                self.ReadPolygon(line, file, mult_coords) # callee appends this line
            elif stripped == 'End Brush':
                return line # let the caller append this line
            else:
                self.lines.append(line)
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
    
    def AdjustTextCoord(self, Normal:int, Pan:int|None, TextureU:int, TextureV:int, mult_coords) -> None:
        if not mult_coords:# TODO: make this work with mult_coords other than (-1,1,1)
            return

        match_n = poly.match(self.lines[Normal])
        match_u = poly.match(self.lines[TextureU])
        match_v = poly.match(self.lines[TextureV])

        nx = float(match_n.group(2))
        ny = float(match_n.group(4))
        nz = float(match_n.group(6))

        ux = float(match_u.group(2))
        uy = float(match_u.group(4))
        uz = float(match_u.group(6))

        vx = float(match_v.group(2))
        vy = float(match_v.group(4))
        vz = float(match_v.group(6))

        # if the Normal has a Y component, that means the X flip has affected it
        if abs(ny) >= 0.01:
            # U is the X position in the texture file, V is the Y position in the texture file
            # so to get the X position in the texture you multiply the location vector by the U vector
            ux *= -1
            vx *= -1
            if Pan is not None:
                # Pan      U=-59 V=0
                match_p = pan_regex.match(self.lines[Pan])
                panu = int(match_p.group(2))
                panv = int(match_p.group(3))
                
                line = '{}U={} V={}{}'.format(match_p.group(1), panu, panv, match_p.group(4))
                self.lines[Pan] = line

        ux = FormatPolyCoord(ux)
        uy = FormatPolyCoord(uy)
        uz = FormatPolyCoord(uz)

        vx = FormatPolyCoord(vx)
        vy = FormatPolyCoord(vy)
        vz = FormatPolyCoord(vz)

        self.lines[TextureU] = match_u.group(1) + '{},{},{}'.format(ux,uy,uz) + match_u.group(8)
        self.lines[TextureV] = match_v.group(1) + '{},{},{}'.format(vx,vy,vz) + match_v.group(8)
    
    def EndPolygon(self, props:dict, first_vert:int, last_vert:int, mult_coords):
        Normal = props['Normal']
        Pan = props.get('Pan')
        TextureU = props['TextureU']
        TextureV = props['TextureV']
        self.AdjustTextCoord(Normal, Pan, TextureU, TextureV, mult_coords)

        i = props.get('Origin')
        if i:
            self.lines[i] = self.AdjustVert(self.lines[i], mult_coords)
        
        for i in range(first_vert, last_vert+1):
            self.lines[i] = self.AdjustVert(self.lines[i], mult_coords)

        if mult_coords:
            polys = self.lines[first_vert:last_vert]
            polys.reverse()
            self.lines[first_vert:last_vert] = polys# MirrorList(self.lines[start:end])
            #print(self.lines[start:end])


    def ReadPolygon(self, line:str, file, mult_coords) -> None:
        props = dict()
        first_vert = None
        while line:
            #print('ReadPolygon', line)
            stripped:str = line.strip()
            match = poly_prop.match(line)
            #print(match.groups())
            key = match.group(2)
            if key=='Vertex' and not first_vert:
                first_vert = len(self.lines)
            else:
                props[key] = len(self.lines)

            self.lines.append(line)
            if stripped == 'End Polygon':
                last_vert = len(self.lines)-2
                # assert we finished with at least 3 vertices
                assert self.lines[last_vert].strip().startswith('Vertex ')
                assert last_vert-first_vert >= 2
                assert last_vert-first_vert < 100
                self.polylist.append([*range(first_vert, last_vert)])
                self.EndPolygon(props, first_vert, last_vert, mult_coords)
                return

            line:str = file.readline()
        
        raise RuntimeError('unexpected end of polygon?')


class Mover(Brush):
    def IsMover(self) -> bool:
        return True
    
    def Finalize(self, mult_coords):
        super().Finalize(mult_coords)
        i = self.GetPropIdx('PostScale')
        if not i:
            line = '    PostScale=(Scale=(X={},Y={},Z={}),SheerAxis=SHEER_ZX)\n'.format(-1,1,1)
            #self.props['PostScale'] = len(self.lines)-1
            self.lines.insert(-1, line)
            raise NotImplementedError('TODO: missing PostScale in Finalize')
        else:
            self.lines[i] = self.FixMoverPostScale(self.lines[i], mult_coords)
        
    
    def EndPolygon(self, props:dict, first_vert:int, last_vert:int, mult_coords):
        pass # Movers use PostScale instead of modifying vertices


def CreateActor(line:str) -> Actor:
    match = getclassname.match(line)
    classname = match.group(1)
    if classname in Actor.mover_classes:
        return Mover(line)
    elif classname in Actor.brush_classes:
        return Brush(line)
    return Actor(line)
