import argparse
from pathlib import Path
from time import sleep
from MapLibs.t3d import Map, GetDefaultOut
import pyperclip

# TODO: arguments to do a single file
parser = argparse.ArgumentParser(description='Unreal Map Flipper/Transformer')
parser.add_argument('--all', action="store_true", help='Do all the maps')
args = parser.parse_args()

# keep the paths short because UnrealEd has a strict limit, I think 80 characters
outdir = Path('C:\\t\\im\\') # GetDefaultOut()
outdir.mkdir(exist_ok=True)
indir = outdir.parent / 'ex'
indir.mkdir(exist_ok=True)
donedir = outdir.parent / 'dx'
donedir.mkdir(exist_ok=True)
mult_coords = (-1,1,1)
mult_coords_desc = str(mult_coords[0])+'_'+str(mult_coords[1])+'_'+str(mult_coords[2])
created = set()

def CreateImport(export:Path, do_sleep=False):
    global created
    outname = export.stem+'_'+mult_coords_desc
    if do_sleep:
        pyperclip.copy(outname)
    if outname in created:
        return outname
    created.add(outname)
    if do_sleep:
        sleep(1) # HACK: make sure the files are fully written

    print('reading', export)
    m = Map()
    m.SetMirror(mult_coords)
    m.Read(export)
    outpath = outdir / (outname+'.t3d')
    m.Write(outpath)
    print('wrote to', outpath)
    return outname


def ReadExport(export:Path):
    outname = CreateImport(export, do_sleep=True)
    #export.unlink()
    dxfile = donedir / (outname+'.dx')
    print('waiting for', dxfile)
    while not dxfile.exists():
        sleep(1)
    print('done with', dxfile)


def DoAll():
    dx = Path(r'C:\Games\DX\Deus Ex Rando\System')
    mapsdir = dx.parent / 'Maps'
    resume=False#
    resumeMap='09_NYC_ShipBelow'

    for export in indir.glob('*.t3d'):
        last_map = export.stem
        export = indir / (last_map+'.t3d')
        CreateImport(export)
    
    # redoing the processing on existing t3d files doesn't care about this, more convenient to die here
    assert len(list(donedir.glob('*')))==0, 'empty '+str(donedir)+' before starting --all'
    for map in mapsdir.glob('*.dx'):
        last_map = map.stem
        if last_map==resumeMap:
            resume=False
        if resume:
            continue
        export = indir / (last_map+'.t3d')
        print('')
        print('')
        if not export.exists():
            pyperclip.copy(last_map)
            print(last_map, 'copied to clipboard, waiting for file', export)
        while not export.exists():
            sleep(0.2)
        ReadExport(export)


if args.all:
    DoAll()
else:
    raise Exception('Need to provide arguments!')
