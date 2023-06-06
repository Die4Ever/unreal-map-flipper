import unittest
from unittest import case
import inspect
import numpy
from typeguard import typechecked, install_import_hook
from pathlib import Path

typechecks = True
if typechecks:
    install_import_hook('MapLibs')

from MapLibs.t3d import *
from MapLibs.actor import *

class MockFile:
    def __init__(self, content:str):
        self.pos = 0
        self.totallen = len(content)
        self.lines = content.split('\n')
        self.sep = ''
    
    def readline(self) -> str:
        s = self.lines[self.pos]
        self.pos += 1
        #print(inspect.stack()[1][3], 'readline:', s)
        return s + self.sep

    def reset(self):
        print(inspect.stack()[1][3], 'MockFile.reset()', self.totallen, len(self.lines))
        self.pos = 0
        self.sep = ''

polygonfile = MockFile(
"""    Begin Polygon Item=OUTSIDE Texture=ClenMedmWalnt_A Flags=32 Link=1
             Origin   -00004.000000,+00068.000000,-00004.000000
             Normal   +00000.000000,+00000.000000,-00001.000000
             TextureU -00000.000000,-00001.000000,-00000.000000
             TextureV -00001.000000,+00000.000000,+00000.000000
             Vertex   -00004.000000,+00072.000000,-00004.000000
             Vertex   +00004.000000,+00072.000000,-00004.000000
             Vertex   +00004.000000,-00072.000000,-00004.000000
             Vertex   -00004.000000,-00072.000000,-00004.000000
          End Polygon
End Test""")

brushfile = MockFile(
"""Begin Actor Class=Brush Name=Brush49
    Begin Brush Name=Model14
       Begin PolyList
          Begin Polygon Item=OUTSIDE Texture=ClenMedmWalnt_A Flags=32 Link=0
             Origin   -00004.000000,-00068.000000,+00004.000000
             Normal   +00000.000000,+00000.000000,+00001.000000
             TextureU +00000.000000,+00001.000000,+00000.000000
             TextureV -00001.000000,+00000.000000,+00000.000000
             Vertex   -00004.000000,-00072.000000,+00004.000000
             Vertex   +00004.000000,-00072.000000,+00004.000000
             Vertex   +00004.000000,+00072.000000,+00004.000000
             Vertex   -00004.000000,+00072.000000,+00004.000000
          End Polygon
       End PolyList
    End Brush
    Brush=Model'MyLevel.Model14'
    PrePivot=(X=4.000000,Y=68.000000,Z=-4.000000)
    Name=Brush49
End Actor
End Test""")

actorfile = MockFile(
"""Begin Map
Begin Actor Class=Jock Name=Jock0
    Orders=Standing
    bLikesNeutral=False
    bHateCarcass=True
    bHateDistress=True
    bReactAlarm=False
    bReactShot=True
    bReactDistress=True
    InitialAlliances(0)=(AllianceName=Player)
    InitialAlliances(1)=(AllianceName=BarFlys)
    InitialInventory(0)=(Inventory=Class'DeusEx.WeaponStealthPistol')
    InitialInventory(1)=(Inventory=Class'DeusEx.Ammo10mm',Count=12)
    InitialInventory(2)=(Inventory=Class'DeusEx.WeaponCombatKnife')
    FootRegion=(Zone=ZoneInfo'MyLevel.ZoneInfo5',iLeaf=492,ZoneNumber=1)
    HeadRegion=(Zone=ZoneInfo'MyLevel.ZoneInfo5',iLeaf=485,ZoneNumber=1)
    ViewRotation=(Yaw=11040)
    VisibilityThreshold=0.000000
    Alliance=BarFlys
    LastRenderTime=139.187988
    DistanceFromPlayer=542.363525
    Level=LevelInfo'MyLevel.LevelInfo0'
    Tag=Jock
    Base=LevelInfo'MyLevel.LevelInfo0'
    Region=(Zone=ZoneInfo'MyLevel.ZoneInfo5',iLeaf=485,ZoneNumber=1)
    Location=(X=-942.777710,Y=-487.315552,Z=48.964230)
    Rotation=(Yaw=11040)
    OldLocation=(X=-866.068909,Y=1041.609253,Z=-16.400154)
    BarkBindName="Man"
    UnfamiliarName="Pilot guy"
    Name=Jock0
End Actor
Begin Actor Class=AmbientSound Name=AmbientSound0
    LastRenderTime=139.187988
    DistanceFromPlayer=3083.201416
    Level=LevelInfo'MyLevel.LevelInfo0'
    Tag=AmbientSound
    Region=(Zone=ZoneInfo'MyLevel.ZoneInfo5',iLeaf=78,ZoneNumber=1)
    Location=(X=-3415.629883,Y=673.263794,Z=59.187805)
    OldLocation=(X=-1396.085693,Y=1057.143433,Z=-53.899948)
    SoundRadius=6
    SoundVolume=100
    AmbientSound=Sound'Ambient.Ambient.EchoWaterDrips'
    Name=AmbientSound0
End Actor
End Map""")

unatcopit = MockFile(
"""Begin Map
Begin Actor Class=Brush Name=Brush359
    CsgOper=CSG_Subtract
    MainScale=(SheerAxis=SHEER_ZX)
    PostScale=(Scale=(X=0.625000,Y=1.454545,Z=2.100000),SheerAxis=SHEER_ZX)
    DistanceFromPlayer=907.171448
    Level=LevelInfo'MyLevel.LevelInfo0'
    Tag=Brush
    Region=(Zone=LevelInfo'MyLevel.LevelInfo0',iLeaf=-1)
    Location=(X=-272.000000,Y=576.000000,Z=240.000000)
    Rotation=(Pitch=16384,Yaw=16384)
    Begin Brush Name=Model354
       Begin PolyList
          Begin Polygon Item=OUTSIDE Texture=Uob_Far_Wall_B Flags=8388608 Link=0
             Origin   -00194.285721,-00128.000000,+00088.000023
             Normal   +00000.000000,+00000.000000,+00001.000000
             TextureU +00000.000000,+00001.250000,+00000.000000
             TextureV -00004.200000,+00000.000000,+00000.000000
             Vertex   -00080.000000,-00128.000000,+00088.000000
             Vertex   +00080.000000,-00128.000000,+00088.000000
             Vertex   +00080.000000,+00128.000000,+00088.000000
             Vertex   -00080.000000,+00128.000000,+00088.000000
          End Polygon
          Begin Polygon Item=OUTSIDE Texture=Uob_Far_Wall_B Flags=8388608 Link=1
             Origin   -00194.285721,+00128.000000,-00088.000023
             Normal   +00000.000000,+00000.000000,-00001.000000
             TextureU +00000.000000,-00001.249999,+00000.000000
             TextureV -00004.200000,+00000.000000,+00000.000000
             Vertex   -00080.000000,+00128.000000,-00088.000000
             Vertex   +00080.000000,+00128.000000,-00088.000000
             Vertex   +00080.000000,-00128.000000,-00088.000000
             Vertex   -00080.000000,-00128.000000,-00088.000000
          End Polygon
          Begin Polygon Item=OUTSIDE Texture=Marker_sky Link=2
             Origin   -00080.000000,+00128.000000,-00088.000000
             Normal   +00000.000000,+00001.000000,+00000.000000
             TextureU +00001.000000,+00000.000000,+00000.000000
             TextureV +00000.000000,+00000.000000,-00001.000000
             Vertex   -00080.000000,+00128.000000,-00088.000000
             Vertex   -00080.000000,+00128.000000,+00088.000000
             Vertex   +00080.000000,+00128.000000,+00088.000000
             Vertex   +00080.000000,+00128.000000,-00088.000000
          End Polygon
          Begin Polygon Item=OUTSIDE Texture=Uob_Far_Wall_B Flags=8388608 Link=3
             Origin   -00194.285721,-00128.000000,-00088.000023
             Normal   +00000.000000,-00001.000000,+00000.000000
             TextureU +00000.000000,+00000.000000,+00002.909090
             TextureV -00004.200000,+00000.000000,+00000.000000
             Vertex   +00080.000000,-00128.000000,-00088.000000
             Vertex   +00080.000000,-00128.000000,+00088.000000
             Vertex   -00080.000000,-00128.000000,+00088.000000
             Vertex   -00080.000000,-00128.000000,-00088.000000
          End Polygon
          Begin Polygon Item=OUTSIDE Texture=UN_Wall_Green Flags=8388608 Link=4
             Origin   +00080.000015,-00307.199921,+00308.000122
             Normal   +00001.000000,+00000.000000,+00000.000000
             TextureU +00000.000000,-00000.625000,+00000.000000
             TextureV +00000.000000,+00000.000000,-00001.454545
             Vertex   +00080.000000,+00128.000000,-00088.000000
             Vertex   +00080.000000,+00128.000000,+00088.000000
             Vertex   +00080.000000,-00128.000000,+00088.000000
             Vertex   +00080.000000,-00128.000000,-00088.000000
          End Polygon
          Begin Polygon Item=OUTSIDE Texture=Marker_sky Link=5
             Origin   -00080.000000,-00128.000000,-00088.000000
             Normal   -00001.000000,+00000.000000,+00000.000000
             TextureU +00000.000000,+00001.000000,+00000.000000
             TextureV +00000.000000,+00000.000000,-00001.000000
             Vertex   -00080.000000,-00128.000000,-00088.000000
             Vertex   -00080.000000,-00128.000000,+00088.000000
             Vertex   -00080.000000,+00128.000000,+00088.000000
             Vertex   -00080.000000,+00128.000000,-00088.000000
          End Polygon
       End PolyList
    End Brush
    Brush=Model'MyLevel.Model354'
    PrePivot=(X=-80.000000,Y=128.000000,Z=-88.000023)
    Name=Brush359
End Actor
End Map""")

@typechecked
class T3DTestCase(unittest.TestCase):
    def test_mirror(self):
        orig = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1] # verticies are counter-clockwise, right?
        desired = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        result = MirrorList(orig)
        self.assertListEqual(result, desired, 'mirror')

    def test_FormatCoord(self):
        s = FormatPolyCoord(1)
        self.assertEqual(s, '+00001.000000')
        s = FormatPolyCoord(-1)
        self.assertEqual(s, '-00001.000000')
        s = FormatPolyCoord(0.1)
        self.assertEqual(s, '+00000.100000')
        s = FormatPolyCoord(-0.1)
        self.assertEqual(s, '-00000.100000')

    def assertRotatorsAlmostEqual(self, r, r2):
        print(r,'vs',r2)
        self.assertTrue( abs(r[0]-r2[0]) <3, 'assertRotatorsAlmostEqual pitch ' +str(r[0])+' vs '+str(r2[0]) )
        self.assertTrue( abs(r[1]-r2[1]) <3, 'assertRotatorsAlmostEqual yaw ' +str(r[1])+' vs '+str(r2[1]) )
        self.assertTrue( abs(r[2]-r2[2]) <3, 'assertRotatorsAlmostEqual roll ' +str(r[2])+' vs '+str(r2[2]) )
    
    def test_rotation_matrix(self):
        RADIANS_TO_UU = 65535 / np.pi / 2

        self.assertAlmostEqual(65535 / RADIANS_TO_UU, 6.28319, 5, 'RADIANS_TO_UU')
        self.assertNotAlmostEqual(65536 / RADIANS_TO_UU, 6.28319, 5, 'RADIANS_TO_UU')
        
        iden_rot_mat = np.array([[1, 0, 0],
                            [0, 1, 0],
                            [0, 0, 1]])
        rot = rotation_matrix(0,0,0)
        numpy.testing.assert_array_almost_equal(rot, iden_rot_mat, 4, 'identity rot matrix')
        rot = rotation_matrix(65535,65535,65535)
        numpy.testing.assert_array_almost_equal(rot, iden_rot_mat, 4, 'identity rot matrix')
        rot = rotation_matrix(-65535,-65535,-65535)
        numpy.testing.assert_array_almost_equal(rot, iden_rot_mat, 4, 'identity rot matrix')

        rot = (0,0,0)
        coords = rotate_mult_coords((1,0,0), rot, rot, (1,1,1))
        numpy.testing.assert_array_almost_equal(coords, (1,0,0), 4, 'rotated mult coords')
        rot = (12454,42643,6953)
        coords = rotate_mult_coords((1,0,0), rot, rot, (1,1,1))
        numpy.testing.assert_array_almost_equal(coords, (1,0,0), 2, 'rotated mult coords')
        rot = (0,0,0)
        coords = rotate_mult_coords((1,2,3), rot, rot, (-1,1,1))
        numpy.testing.assert_array_almost_equal(coords, (-1,2,3), 4, 'rotated mult coords')
        rot = (0,16384,0)
        coords = rotate_mult_coords((1,2,3), rot, rot, (-1,1,1))
        numpy.testing.assert_array_almost_equal(coords, (1,-2,3), 4, 'rotated mult coords')

    def test_rotators(self):
        # people talking in bar
        print('try to fix the people in the bar')
        man_yaw = -43264 # 22271 in positive terms, but this is what the map file says
        man_positive_yaw = 22271
        man_desired_yaw = 10496
        woman_yaw = -71024 # -5489 normalized, or 60046 in positive, but this is what the map file says
        woman_desired_yaw = 38256 # or -27279
        pinball_yaw = -32872
        pinball_desired_yaw = 32872 # or -32663
        rot_offset = 16384

        rm = mirror_rotation((0, man_yaw, 0), rot_offset)
        self.assertRotatorsAlmostEqual(rm, (0, man_desired_yaw, 0))
        rm = mirror_rotation((0, man_positive_yaw, 0), rot_offset)
        self.assertRotatorsAlmostEqual(rm, (0, man_desired_yaw, 0))
        rm = mirror_rotation((0, woman_yaw, 0), rot_offset)
        self.assertRotatorsAlmostEqual(rm, (0, woman_desired_yaw, 0))
        rot_offset = classes_rot_offsets['Pinball']
        rm = mirror_rotation((0, pinball_yaw, 0), rot_offset)
        self.assertRotatorsAlmostEqual(rm, (0, pinball_desired_yaw, 0))
    
    def test_read_polygon(self):
        polygonfile.reset()
        actor:Brush = CreateActor(None, 'Begin Actor Class=Brush Name=Test1')
        self.assertEqual(actor.classname, 'Brush')
        actor.ReadPolygon(polygonfile.readline(), polygonfile, None)

        self.assertEqual(actor.lines[0], 'Begin Actor Class=Brush Name=Test1')
        self.assertEqual(actor.lines[1], '    Begin Polygon Item=OUTSIDE Texture=ClenMedmWalnt_A Flags=32 Link=1')
        self.assertEqual(actor.lines[-1], '          End Polygon')
        self.assertEqual(polygonfile.readline(), 'End Test')

    def test_read_brush(self):
        print('test ReadBrush first')
        brushfile.reset()
        actor:Brush = CreateActor(None, brushfile.readline())
        self.assertEqual(actor.classname, 'Brush')
        ret = actor.ReadBrush(brushfile.readline(), brushfile, None)

        self.assertEqual(actor.lines[0], 'Begin Actor Class=Brush Name=Brush49')
        self.assertEqual(actor.lines[1], '    Begin Brush Name=Model14')
        self.assertEqual(actor.lines[-1], '       End PolyList')
        self.assertEqual(ret, '    End Brush')
        self.assertEqual(brushfile.readline(), '    Brush=Model\'MyLevel.Model14\'')
        self.assertTrue(isinstance(actor, Brush))
        self.assertFalse(isinstance(actor, Mover))

        print('now test Actor::Read')
        brushfile.reset()
        actor:Brush = CreateActor(None, brushfile.readline())
        self.assertEqual(actor.classname, 'Brush')
        actor.Read(brushfile, None)

        self.assertEqual(actor.lines[0], 'Begin Actor Class=Brush Name=Brush49')
        self.assertEqual(actor.lines[1], '    Begin Brush Name=Model14')
        self.assertEqual(actor.lines[-1], 'End Actor')
        self.assertEqual(brushfile.readline(), 'End Test')
        try:
            self.assertEqual(len(str(actor)), 880, 'string of actor length')
        except Exception as e:
            print('ERROR!')
            print(str(actor))
            print(e)
            raise

    def test_read_actor(self):
        actorfile.reset()
        self.assertEqual(actorfile.readline(), 'Begin Map')
        actor = CreateActor(None, actorfile.readline())
        self.assertEqual(actor.classname, 'Jock')
        self.assertFalse(isinstance(actor, Brush))
        actor.Read(actorfile, None)

        self.assertEqual(actorfile.readline(), 'Begin Actor Class=AmbientSound Name=AmbientSound0')

    def test_read_map(self):
        actorfile.reset()
        map = Map()
        map.SetMirror((-1,1,1))
        map._Read(actorfile)

        self.assertEqual(len(map.actors), 2)

        actorfile.reset()
        actorfile.sep = '\r\n'# test with newlines
        map = Map()
        map.SetMirror((1,-1,1))
        map._Read(actorfile)

        self.assertEqual(len(map.actors), 2)

    def test_map_file_mirror_x(self):
        m = Map()
        out = GetDefaultOut()
        root = out.parent
        f = root / 'tests' / 'RotationTest.t3d'
        m.SetMirror((-1,1,1))
        m.Read(f)
        f = out / 't_mirror_x.t3d'
        m.Write(f)

    def test_map_file_mirror_y(self):
        m = Map()
        out = GetDefaultOut()
        root = out.parent
        f = root / 'tests' / 'RotationTest.t3d'
        m.SetMirror((1,-1,1))
        m.Read(f)
        f = out / 't_mirror_y.t3d'
        m.Write(f)
    
    def test_map_file_bigger(self):
        m = Map()
        out = GetDefaultOut()
        root = out.parent
        f = root / 'tests' / 'RotationTest.t3d'
        m.SetMirror((1.5,1.5,1.5))
        m.Read(f)
        f = out / 't_bigger.t3d'
        m.Write(f)
    
    def test_map_file_smaller(self):
        m = Map()
        out = GetDefaultOut()
        root = out.parent
        f = root / 'tests' / 'RotationTest.t3d'
        m.SetMirror((0.7,0.7,0.7))
        m.Read(f)
        f = out / 't_smaller.t3d'
        m.Write(f)

    def test_unatco_pit(self):
        unatcopit.reset()
        unatcopit.sep = '\r\n'# test with newlines
        map = Map()
        map.SetMirror((-1,1,1))
        map._Read(unatcopit)
        print(map.ToString())



if __name__ == "__main__":
    unittest.main(verbosity=9, warnings="error", failfast=True)
