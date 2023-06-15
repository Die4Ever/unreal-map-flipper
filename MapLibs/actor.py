from MapLibs.t3d import *
import re
import numpy as np

coord = r'((\+|-)\d+\.\d+)'
poly = re.compile(r'^(\s*\w+\s+)'+coord+','+coord+','+coord+r'(\s*$)')

poly_prop = re.compile(r'^(\s*)(\w+)(\s+)(.*)$')

flags_regex = re.compile(r'^\s*Begin Polygon.*Flags=(\d+)\s+.*$')

pan_regex = re.compile(r'^(\s+Pan\s+)U=([^\s]+)\s+V=([^\s]+)(\s*)$')

coord = r'(-?\d+(\.\d+)?)'
vect_pattern = r'\((X=' + coord + ')?,?(Y=' + coord + ')?,?(Z=' + coord + ')?\)'
vect_regex = re.compile(vect_pattern)
loc = re.compile(r'^(\s+[^=]+)=' + vect_pattern + r'(\s*)$')

axis = r'(-?\d+)'
rot = re.compile(r'^(\s+[^=]+)=\((Pitch=' +axis+ r')?,?(Yaw=' +axis+ r')?,?(Roll=' +axis+ r')?\)(\s*)$')

getclassname = re.compile(r'^Begin Actor Class=([^\s]+) Name=([^\s]+)\s*$')

prop_regex = re.compile(r'^(\s*)([^=]+)=(.*)$')

scale_regex = re.compile(r'^([^=]+)=\((Scale=' + vect_pattern + r',)?(.*\))(\s*)$')


# some models like the pinball machine are sideways, so the math doesn't match the appearance
# default is 16384 not 0, at least for ScriptedPawns
classes_rot_offsets = dict(
    Teleporter=16384, # TODO: check these 2...
    PlayerStart=16384,
    Pinball=32768,
    Chair1=32768,
    ComputerPersonal=32768,
    Brush=0,
    ATM=16384,
    ComputerPublic=16384,
    ComputerSecurity=16384,
    CigaretteMachine=16384,
    VendingMachine=16384,
    WaterFountain=16384,
    SecurityCamera=16384,
    RetinalScanner=16384,
    AutoTurret=16384,
    AutoTurretSmall=16384,
    ControlPanel=16384,
    BobPageAugmented=16384,
    Mailbox=16384,
    Keypad=16384,
    Keypad1=16384,
    Keypad2=16384,
    Keypad3=16384,
    LuciusDeBeers=16384,
    Switch1=16384,
    Switch2=16384,
    AlarmUnit=16384,
    Faucet=16384,
    CageLight=16384,
    ShowerFaucet=16384,
    ShowerHead=16384,
    LightSwitch=16384,

    # auto generated list of Decorations (any non-zero values should be moved above this line):
    DeusExDecoration=0,
    AIPrototype=0,
    AlarmLight=0,
    Basketball=0,
    BoneFemur=0,
    BoneSkull=0,
    Button1=0,
    Cart=0,
    CeilingFan=0,
    CeilingFanMotor=0,
    Containers=0,
    AmmoCrate=0,
    Barrel1=0,
    BarrelAmbrosia=0,
    BarrelFire=0,
    BarrelVirus=0,
    Basket=0,
    BoxLarge=0,
    BoxMedium=0,
    BoxSmall=0,
    CrateBreakableMedCombat=0,
    CrateBreakableMedGeneral=0,
    CrateBreakableMedMedical=0,
    CrateExplosiveSmall=0,
    CrateUnbreakableLarge=0,
    CrateUnbreakableMed=0,
    CrateUnbreakableSmall=0,
    Trashbag=0,
    Trashbag2=0,
    TrashCan1=0,
    Trashcan2=0,
    TrashCan3=0,
    TrashCan4=0,
    DentonClone=0,
    ElectronicDevices=0,
    Computers=0,
    HackableDevices=0,
    AcousticSensor=0,
    AutoTurretGun=0,
    AutoTurretGunSmall=0,
    Phone=0,
    TAD=0,
    Fan1=0,
    Fan1Vertical=0,
    Fan2=0,
    FlagPole=0,
    Flask=0,
    Flowers=0,
    Furniture=0,
    CoffeeTable=0,
    Cushion=0,
    Lamp=0,
    Lamp1=0,
    Lamp2=0,
    Lamp3=0,
    Seat=0,
    ChairLeather=0,
    CouchLeather=0,
    HKChair=0,
    HKCouch=0,
    OfficeChair=0,
    WHBenchEast=0,
    WHBenchLibrary=0,
    WHChairDining=0,
    WHChairOvalOffice=0,
    WHChairPink=0,
    WHRedCouch=0,
    HangingDecoration=0,
    Chandelier=0,
    ClothesRack=0,
    HangingChicken=0,
    HangingShopLight=0,
    HKBirdcage=0,
    HKHangingLantern=0,
    HKHangingLantern2=0,
    HKHangingPig=0,
    HKMarketLight=0,
    PoolTableLight=0,
    TrafficLight=0,
    HongKongDecoration=0,
    HKBuddha=0,
    HKIncenseBurner=0,
    HKMarketTable=0,
    HKMarketTarp=0,
    HKTable=0,
    HKTukTuk=0,
    InformationDevices=0,
    BookClosed=0,
    BookOpen=0,
    DataCube=0,
    Newspaper=0,
    NewspaperOpen=0,
    LifeSupportBase=0,
    Lightbulb=0,
    Microscope=0,
    NewYorkDecoration=0,
    NYEagleStatue=0,
    NYLiberty=0,
    NYLibertyTop=0,
    NYLibertyTorch=0,
    OutdoorThings=0,
    Buoy=0,
    Bushes1=0,
    Bushes2=0,
    Bushes3=0,
    Cactus1=0,
    Cactus2=0,
    CarBurned=0,
    CarStripped=0,
    CarWrecked=0,
    DXLogo=0,
    DXText=0,
    Earth=0,
    EidosLogo=0,
    FirePlug=0,
    IonStormLogo=0,
    Moon=0,
    SatelliteDish=0,
    StatueLion=0,
    Tree=0,
    Tree1=0,
    Tree2=0,
    Tree3=0,
    Tree4=0,
    Pan1=0,
    Pan2=0,
    Pan3=0,
    Pan4=0,
    Pillow=0,
    Plant1=0,
    Plant2=0,
    Plant3=0,
    Poolball=0,
    Pot1=0,
    Pot2=0,
    RoadBlock=0,
    ShipsWheel=0,
    ShopLight=0,
    SignFloor=0,
    SubwayControlPanel=0,
    Toilet=0,
    Toilet2=0,
    Trash=0,
    TrashPaper=0,
    Tumbleweed=0,
    Trophy=0,
    Valve=0,
    Vase1=0,
    Vase2=0,
    Vehicles=0,
    AttackHelicopter=0,
    BlackHelicopter=0,
    MiniSub=0,
    NYPoliceBoat=0,
    Van=0,
    WashingtonDecoration=0,
    WHBookstandLibrary=0,
    WHCabinet=0,
    WHDeskLibrarySmall=0,
    WHDeskOvalOffice=0,
    WHEndtableLibrary=0,
    WHFireplaceGrill=0,
    WHFireplaceLog=0,
    WHPhone=0,
    WHPiano=0,
    WHRedCandleabra=0,
    WHRedEagleTable=0,
    WHRedLampTable=0,
    WHRedOvalTable=0,
    WHRedVase=0,
    WHTableBlue=0,
    WaterCooler=0,
    Carcass=0,
    DeusExCarcass=0,
    AlexJacobsonCarcass=0,
    AnnaNavarreCarcass=0,
    BartenderCarcass=0,
    BoatPersonCarcass=0,
    BobPageCarcass=0,
    BumFemaleCarcass=0,
    BumMale2Carcass=0,
    BumMale3Carcass=0,
    BumMaleCarcass=0,
    Businessman1Carcass=0,
    Businessman2Carcass=0,
    Businessman3Carcass=0,
    Businesswoman1Carcass=0,
    ButlerCarcass=0,
    CatCarcass=0,
    ChadCarcass=0,
    ChefCarcass=0,
    ChildMale2Carcass=0,
    ChildMaleCarcass=0,
    CopCarcass=0,
    DobermanCarcass=0,
    DoctorCarcass=0,
    Female1Carcass=0,
    Female2Carcass=0,
    Female3Carcass=0,
    Female4Carcass=0,
    FordSchickCarcass=0,
    GarySavageCarcass=0,
    GilbertRentonCarcass=0,
    GordonQuickCarcass=0,
    GrayCarcass=0,
    GreaselCarcass=0,
    GuntherHermannCarcass=0,
    HarleyFilbenCarcass=0,
    HKMilitaryCarcass=0,
    Hooker1Carcass=0,
    Hooker2Carcass=0,
    HowardStrongCarcass=0,
    JaimeReyesCarcass=0,
    JanitorCarcass=0,
    JCDentonMaleCarcass=0,
    JockCarcass=0,
    JoeGreeneCarcass=0,
    JoJoFineCarcass=0,
    JordanSheaCarcass=0,
    JosephManderleyCarcass=0,
    JuanLebedevCarcass=0,
    JunkieFemaleCarcass=0,
    JunkieMaleCarcass=0,
    KarkianBabyCarcass=0,
    KarkianCarcass=0,
    LowerClassFemaleCarcass=0,
    LowerClassMale2Carcass=0,
    LowerClassMaleCarcass=0,
    MaggieChowCarcass=0,
    MaidCarcass=0,
    Male1Carcass=0,
    Male2Carcass=0,
    Male3Carcass=0,
    Male4Carcass=0,
    MargaretWilliamsCarcass=0,
    MaxChenCarcass=0,
    MechanicCarcass=0,
    MIBCarcass=0,
    MichaelHamnerCarcass=0,
    MJ12CommandoCarcass=0,
    MJ12TroopCarcass=0,
    MorganEverettCarcass=0,
    MuttCarcass=0,
    NathanMadisonCarcass=0,
    NicoletteDuClareCarcass=0,
    NurseCarcass=0,
    PaulDentonCarcass=0,
    PhilipMeadCarcass=0,
    PigeonCarcass=0,
    RachelMeadCarcass=0,
    RatCarcass=0,
    RiotCopCarcass=0,
    SailorCarcass=0,
    SamCarterCarcass=0,
    SandraRentonCarcass=0,
    SarahMeadCarcass=0,
    ScientistFemaleCarcass=0,
    ScientistMaleCarcass=0,
    ScubaDiverCarcass=0,
    SeagullCarcass=0,
    SecretaryCarcass=0,
    SecretServiceCarcass=0,
    SmugglerCarcass=0,
    SoldierCarcass=0,
    StantonDowdCarcass=0,
    TerroristCarcass=0,
    TerroristCommanderCarcass=0,
    ThugMale2Carcass=0,
    ThugMale3Carcass=0,
    ThugMaleCarcass=0,
    TiffanySavageCarcass=0,
    TobyAtanweCarcass=0,
    TracerTongCarcass=0,
    TriadLumPath2Carcass=0,
    TriadLumPathCarcass=0,
    TriadRedArrowCarcass=0,
    UNATCOTroopCarcass=0,
    WaltonSimonsCarcass=0,
    WIBCarcass=0,
    ScaledSprite=0,
)

def rotation_matrix(x, y, z):
    RADIANS_TO_UU = 65535 / np.pi / 2
    x = float(x) / RADIANS_TO_UU
    y = float(y) / RADIANS_TO_UU
    z = float(z) / RADIANS_TO_UU

    c1 = np.cos(x)
    s1 = np.sin(x)
    c2 = np.cos(y)
    s2 = np.sin(y)
    c3 = np.cos(z)
    s3 = np.sin(z)

    matrix=np.array([[c2*c3, -c2*s3, s2],
                        [c1*s3+c3*s1*s2, c1*c3-s1*s2*s3, -c2*s1],
                        [s1*s3-c1*c3*s2, c3*s1+c1*s2*s3, c1*c2]])

    return matrix

def rotate_mult_coords(coords, rot, newrot, mult_coords):
    if mult_coords is None:
        return None
    
    a = rot[0]
    b = rot[1]
    c = rot[2]
    rot_mat = rotation_matrix(a, c, b)
    coords = np.dot(rot_mat, coords)

    coords *= mult_coords

    a = newrot[0]
    b = newrot[1]
    c = newrot[2]
    rot_mat = rotation_matrix(-a, -c, -b)
    coords = np.dot(rot_mat, coords)
    return coords


# keep list of vertices counter-clockwise
def MirrorList(l):
    # ensure proper vertex order
    return l[0:1] + l[-1:0:-1]


def mirror_rotation(r, offset):
    yaw = int(r[1])
    yaw += offset # offset by 16384 because we want to align with north/south not west/east, if this was a clock we want yaw 0 to be 12 o'clock
    yaw %= 65535 # 65535 is more accurate than 65536, I guess it's true that 65535 is 360 degrees and not 65536
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
        self.parent = None
        self.oldRot = (0,0,0)
        self.newRot = (0,0,0)
        self.oldPrePivot = (0,0,0)
        self.newPrePivot = (0,0,0)
    

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
    
    def GetPropIdx(self, prop:str) -> int|None:
        return self.props.get(prop)
    
    def IterProps(self, *p) -> list:
        ret = []
        for prop in p:
            if prop in self.props:
                ret.append(self.GetPropIdx(prop))
        return ret


    def Finalize(self, mult_coords):# TODO: more checks in finalize
        i = self.GetPropIdx('Rotation')
        if i:
            self.oldRot = self.GetRot(self.lines[i])[0:3]

        if not isinstance(self, Brush):
            if not self.GetPropIdx('Rotation'):
                self.props['Rotation'] = len(self.lines)-2
                line = '    Rotation=(Pitch=0,Yaw=0,Roll=0)\n' # stick this default in so we can correct it below
                self.lines.insert(-2, line) # don't overwrite the End Actor

            for i in self.IterProps('Rotation', 'BaseRot', 'SavedRot', 'ViewRotation'):
                self.lines[i] = self.ProcRot(self.lines[i], mult_coords)

        i = self.GetPropIdx('Rotation')
        if i:
            self.newRot = self.GetRot(self.lines[i])[0:3]

        for i in self.IterProps('Location', 'BasePos', 'SavedPos', 'OldLocation'):
            self.lines[i] = self.ProcLoc(self.lines[i], mult_coords)

        self._Finalize(mult_coords)

    def _Finalize(self, mult_coords):
        pass

    def GetLoc(self, line:str) -> tuple:
        match = loc.match(line)

        x = match.group(3)
        if not x:
            x = 0
        x = float(x)

        y = match.group(6)
        if not y:
            y = 0
        y = float(y)

        z = match.group(9)
        if not z:
            z = 0
        z = float(z)

        return (x,y,z,match)


    def ProcLoc(self, line:str, mult_coords) -> str:
        if mult_coords is None:
            return line
        
        (x,y,z,match) = self.GetLoc(line)
        x = float(x) * mult_coords[0]
        y = float(y) * mult_coords[1]
        z = float(z) * mult_coords[2]

        line = match.group(1) + '=(X={:f},Y={:f},Z={:f})'.format(x,y,z) + match.group(11)
        return line
    

    def _ProcLocRot(self, line:str, mult_coords, oldRot, newRot) -> str:
        if mult_coords is None:
            return line
        
        (x,y,z,match) = self.GetLoc(line)
        coords = rotate_mult_coords((x,y,z), oldRot, newRot, mult_coords)

        line = match.group(1) + '=(X={},Y={},Z={})'.format(x,y,z) + match.group(11)
        return line
    
    def ProcLocRot(self, line:str, mult_coords) -> str:
        return self._ProcLocRot(line, mult_coords, self.oldRot, self.newRot)
    

    def GetRot(self, line:str) -> tuple:
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
        
        return (int(pitch), int(yaw), int(roll), match)
    

    def ProcRot(self, line:str, mult_coords:tuple|None) -> str:
        if mult_coords is None:
            return line
        
        (pitch, yaw, roll, match) = self.GetRot(line)

        # TODO: this is only correct when mirroring X or Y
        # temporary variable to get classes_rot_offsets, all Brushes are the same
        classname = self.classname
        if isinstance(self, Brush):
            classname = 'Brush'
        rot_offset = classes_rot_offsets.get(classname, 16384)

        # if flip X
        if mult_coords[0] < 0 and mult_coords[1] > 0:
            (pitch, yaw, roll) = mirror_rotation((pitch,yaw,roll), rot_offset)
        # elif flip Y
        elif mult_coords[1] < 0 and mult_coords[0] > 0:
            rot_offset += 16384
            (pitch, yaw, roll) = mirror_rotation((pitch,yaw,roll), rot_offset)

        line = match.group(1) + '=(Pitch={:d},Yaw={:d},Roll={:d})'.format(pitch,yaw,roll) + match.group(8)
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
                return
            line:str = file.readline()
        
        raise RuntimeError('unexpected end of actor?')
    

    def ReadBrush(self, line:str, file, mult_coords) -> str:
        raise RuntimeError('unexpected Brush in class '+self.classname)


class OldBrush(Actor): # well this was a big waste of time? lol
    def _Finalize(self, mult_coords):# TODO: more checks in finalize
        super()._Finalize(mult_coords)
        if type(self) == OldBrush:
            self.MirrorVerts(mult_coords)

    def MirrorVerts(self, mult_coords):
        i = self.GetPropIdx('PrePivot')
        if i and mult_coords is not None:
            (x,y,z,match) = self.GetLoc(self.lines[i])
            self.lines[i] = self.ProcLoc(self.lines[i], mult_coords)
            self.oldPrePivot = (x,y,z)
            (x,y,z,match) = self.GetLoc(self.lines[i])
            self.newPrePivot = (x,y,z)
        
        for p in self.polylist:
            self.FinalizePolygon(p, mult_coords)
        
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
        if mult_coords is None:
            return line
        match = poly.match(line)
        x = float(match.group(2))
        y = float(match.group(4))
        z = float(match.group(6))

        x -= self.oldPrePivot[0]
        y -= self.oldPrePivot[1]
        z -= self.oldPrePivot[2]

        coords = rotate_mult_coords((x,y,z), self.oldRot, self.newRot, mult_coords)

        x = FormatPolyCoord(coords[0] + self.newPrePivot[0])
        y = FormatPolyCoord(coords[1] + self.newPrePivot[1])
        z = FormatPolyCoord(coords[2] + self.newPrePivot[2])

        line = match.group(1) + '{},{},{}'.format(x,y,z) + match.group(8)
        return line
    
    def AdjustTextCoord(self, Normal:int, Pan:int|None, TextureU:int, TextureV:int, mult_coords) -> None:
        if mult_coords is None:
            return

        match_u = poly.match(self.lines[TextureU])
        match_v = poly.match(self.lines[TextureV])

        ux = float(match_u.group(2))
        uy = float(match_u.group(4))
        uz = float(match_u.group(6))

        vx = float(match_v.group(2))
        vy = float(match_v.group(4))
        vz = float(match_v.group(6))

        # U is the X position in the texture file, V is the Y position in the texture file
        # so to get the X position in the texture you multiply the location vector by the U vector
        ux /= mult_coords[0]
        uy /= mult_coords[1]
        uz /= mult_coords[2]

        vx /= mult_coords[0]
        vy /= mult_coords[1]
        vz /= mult_coords[2]

        ux = FormatPolyCoord(ux)
        uy = FormatPolyCoord(uy)
        uz = FormatPolyCoord(uz)

        vx = FormatPolyCoord(vx)
        vy = FormatPolyCoord(vy)
        vz = FormatPolyCoord(vz)

        self.lines[TextureU] = match_u.group(1) + '{},{},{}'.format(ux,uy,uz) + match_u.group(8)
        self.lines[TextureV] = match_v.group(1) + '{},{},{}'.format(vx,vy,vz) + match_v.group(8)
    

    def FinalizePolygon(self, props:dict, mult_coords):
        first_vert:int = props['first_vert']
        last_vert:int = props['last_vert']
        Normal:int = props['Normal']
        Pan:int|None = props.get('Pan')
        TextureU:int = props['TextureU']
        TextureV:int = props['TextureV']
        self.AdjustTextCoord(Normal, Pan, TextureU, TextureV, mult_coords)

        i = props.get('Origin')
        if i:
            self.lines[i] = self.AdjustVert(self.lines[i], mult_coords)
        
        for i in range(first_vert, last_vert+1):
            self.lines[i] = self.AdjustVert(self.lines[i], mult_coords)

        # only invert if odd number of flips
        num_flips:int = 0
        if mult_coords is not None:
            num_flips = int(mult_coords[0]<0) + int(mult_coords[1]<0) + int(mult_coords[2]<0)
        if num_flips % 2 == 1:
            polys = self.lines[first_vert:last_vert]
            polys.reverse()
            self.lines[first_vert:last_vert] = polys
            #print(polys)


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
                self.polylist.append({'first_vert': first_vert, 'last_vert': last_vert, **props})
                return

            line:str = file.readline()

        raise RuntimeError('unexpected end of polygon?')


class Brush(OldBrush):
    def _Finalize(self, mult_coords):
        super()._Finalize(mult_coords)

        # check if this is a portal
        for p in self.polylist:
            begin = self.lines[p['Begin']]
            flags = flags_regex.match(begin)
            if flags:
                flags = int(flags.group(1))
            # if portal, increase the size slightly to fix rounding issues (vandenberg tunnels, of course)
            if flags and flags & 67108864:
                mult_coords = (mult_coords[0]*1.001, mult_coords[1]*1.001, mult_coords[2]*1.001)
                break

        i = self.GetPropIdx('PostScale')
        if not i and mult_coords is not None:
            line = '    PostScale=(Scale=(X={:f},Y={:f},Z={:f}),SheerAxis=SHEER_ZX)\n'.format(mult_coords[0], mult_coords[1], mult_coords[2])
            self.props['PostScale'] = len(self.lines)-1
            self.lines.insert(-1, line)
        elif i:
            self.lines[i] = self.FixScale(self.lines[i], mult_coords)
        
    
    def FixScale(self, line:str, mult_coords) -> str:
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
        line = m.group(1) + '=(Scale=' + '(X={:f},Y={:f},Z={:f})'.format(x,y,z) + ',' + m.group(12) + m.group(13)
        return line


class Mover(Brush):
    def _Finalize(self, mult_coords):
        super()._Finalize(mult_coords)
        
        for (prop, i) in self.props.items():
            if prop.startswith('KeyPos('):
                self.lines[i] = self.ProcLoc(self.lines[i], mult_coords) # idk if this needs to be ProcLoc or ProcLocRot, will need to find an example


class DeusExLevelInfo(Actor):
    def _Read(self, file, mult_coords:tuple|None):
        super()._Read(file, mult_coords)
        i = self.GetPropIdx('MapName')
        if i and self.parent:
            match = prop_regex.match(self.lines[i])
            self.parent.SetMapName(match.group(3))


def CreateActor(parent, line:str) -> Actor:
    match = getclassname.match(line)
    classname = match.group(1)
    if classname in Actor.mover_classes:
        a = Mover(line)
    elif classname in Actor.brush_classes:
        a = Brush(line)
    elif classname == 'DeusExLevelInfo':
        a = DeusExLevelInfo(line)
    else:
        a = Actor(line)
    a.parent = parent
    return a
