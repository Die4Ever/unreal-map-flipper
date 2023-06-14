from pathlib import Path
from time import sleep
from MapLibs.t3d import Map, GetDefaultOut
import pyperclip

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


def ProcFile(source:Path, dest:Path, mult:tuple):
    print('source:', source, 'dest:', dest, 'mult:', mult)
    m = Map()
    m.SetMirror(mult)
    m.Read(source)
    m.Write(dest)


def CreateImport(export:Path, do_sleep=False):
    global created
    outname = export.stem+'_'+mult_coords_desc
    if outname in created:
        if do_sleep:
            pyperclip.copy(outname)
        return outname
    created.add(outname)
    if do_sleep:
        sleep(1) # HACK: make sure the files are fully written

    outpath = outdir / (outname+'.t3d')
    ProcFile(export, outpath, mult_coords)
    if do_sleep:
        pyperclip.copy(outname)
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

