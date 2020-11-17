import sys, pathlib, ezdxf
from svgwrite.container import SVG
import svgbuilder, log
from convertDXF import *

### I/O ###                     # TODO to be decided by Vectorworks API
dwg_file = '26470A7.dwg'       # TODO currently not used. Vectorworks API will load chosen DWG, export it to DXF, and use the exported DXF as it's intermediary file
dxf_file = '26470A7.dxf'
svg_file = '26470A7.svg'

### Constants ###                   # TODO to be decided by the Vectorworks API
LIBREDWG_DIR = pathlib.Path(__file__).parent.joinpath('files').absolute()
DWG_PATH = LIBREDWG_DIR.joinpath(dwg_file).absolute()
DXF_PATH = LIBREDWG_DIR.joinpath(dxf_file).absolute()
SVG_PATH = LIBREDWG_DIR.joinpath(svg_file).absolute()

### PROGRAM ###
log.to('./files/_log.txt', True)
try:
    svgbuilder.build(DXF_PATH, SVG_PATH)
except IOError:
    print(f'Not a DXF file or a generic I/O error.')
    sys.exit(1)
except ezdxf.DXFStructureError:
    print(f'Invalid or corrupted DXF file.')
    sys.exit(2)
