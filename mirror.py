import argparse
from pathlib import Path
import re
from MapLibs import commands

# TODO: arguments to do a single file
parser = argparse.ArgumentParser(description='Unreal Map Flipper/Transformer')
parser.add_argument('--all', action="store_true", help='Do all the maps')
parser.add_argument('--source', help='Input t3d file')
parser.add_argument('--dest', help='Output t3d file')
parser.add_argument('--mult', help='Multiplication vector in the format of (-1,1,1)')
args = parser.parse_args()


if args.all:
    commands.DoAll()
elif args.source and args.dest and args.mult:
    source = Path(args.source)
    assert source.is_file()
    dest = Path(args.dest)
    assert dest.parent.is_dir()
    mult_match = re.match(r'^\s*\(\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^,]+)\s*\)\s*$', args.mult)
    x = float(mult_match.group(1))
    y = float(mult_match.group(2))
    z = float(mult_match.group(3))
    mult_coords = (x,y,z,)
    commands.ProcFile(source, dest, mult_coords)
else:
    raise Exception('Need to provide arguments!')
