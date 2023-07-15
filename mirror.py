import argparse
from pathlib import Path
import re
from MapLibs import commands

# TODO: arguments to do a single file
parser = argparse.ArgumentParser(description='Unreal Map Flipper/Transformer')
parser.add_argument('--all', action="store_true", help='Do all the maps')
parser.add_argument('--dxrando', action="store_true", help='Do all the DXRando maps')
parser.add_argument('--source', help='Input t3d file')
parser.add_argument('--dest', help='Output t3d file')
parser.add_argument('--mult', help='Multiplication vector in the format of (-1,1,1)')
args = parser.parse_args()


if args.dxrando:
    commands.DXRando()
elif args.all:
    commands.DoAll()
elif args.source and args.dest and args.mult:
    source = Path(args.source)
    assert source.is_file()
    dest = Path(args.dest)
    assert dest.parent.is_dir()
    coord_re = r'\s*([^,]+)\s*'
    mult_re = r'\s*\(' + coord_re+','+coord_re+','+coord_re + r'\)\s*'
    mult_match = re.match(mult_re, args.mult)
    x = float(mult_match.group(1))
    y = float(mult_match.group(2))
    z = float(mult_match.group(3))
    mult_coords = (x,y,z,)
    if x==1 and y==1 and z==1:
        mult_coords = None
    commands.ProcFile(source, dest, mult_coords)
else:
    parser.print_help()
    raise Exception('Need to provide arguments!')
