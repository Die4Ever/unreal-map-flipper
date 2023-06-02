import argparse
from pathlib import Path
from time import sleep
from MapLibs.t3d import Map, GetDefaultOut
import pyperclip

# TODO: arguments to do a single file
parser = argparse.ArgumentParser(description='Unreal Map Flipper/Transformer')
parser.add_argument('--all', action="store_true", help='Do all the maps')
args = parser.parse_args()

outdir = GetDefaultOut()
indir = outdir.parent / 'in'
indir.mkdir(exist_ok=True)
assert len(list(indir.glob('*')))==0, 'empty '+indir+' before starting'
donedir = outdir.parent / 'maps'
donedir.mkdir(exist_ok=True)
assert len(list(donedir.glob('*')))==0, 'empty '+donedir+' before starting'
mult_coords = (-1,1,1)
mult_coords_desc = str(mult_coords[0])+'_'+str(mult_coords[1])+'_'+str(mult_coords[2])
last_map = None


def ReadExport(export:Path):
    outname = export.stem+'_'+mult_coords_desc
    pyperclip.copy(outname)
    sleep(1) # HACK: make sure the files are fully written
    print('reading', export)
    m = Map()
    m.SetMirror(mult_coords)
    m.Read(export)
    outpath = outdir / (outname+'.t3d')
    m.Write(outpath)
    print('wrote to', outpath)
    export.unlink()
    dxfile = donedir / (outname+'.dx')
    print('waiting for', dxfile)
    while not dxfile.exists():
        sleep(1)
    print('done with', dxfile)


def DoAll():
    global last_map
    dx = Path(r'C:\Games\DX\Deus Ex Rando\System')
    mapsdir = dx.parent / 'Maps'
    for map in mapsdir.glob('*.dx'):
        last_map = map.stem
        export = indir / (last_map+'.t3d')
        print('')
        print('')
        print(last_map, 'copied to clipboard, waiting for file', export)
        pyperclip.copy(last_map)
        while not export.exists():
            sleep(0.2)
        ReadExport(export)


if args.all:
    DoAll()
else:
    raise Exception('Need to provide arguments!')
