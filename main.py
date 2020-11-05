import sys, pathlib, ezdxf
from libredwg import *
from ezdxf import recover
from convertDXF import *

### I/O ###
dwg_file = "INPUT FILE HERE.dwg"
dxf_file = "INTERMEDIATE FILE HERE.dxf"
svg_file = "OUTPUT FILE HERE.svg"
# ^ TODO to be decided by Vectorworks API

### Constants ###
LIBREDWG_DIR = pathlib.Path(__file__).parent.joinpath('libredwg').absolute()
DWG_PATH = LIBREDWG_DIR.joinpath(dwg_file).absolute() 
DXF_PATH = LIBREDWG_DIR.joinpath(dxf_file).absolute() 
SVG_PATH = LIBREDWG_DIR.joinpath(svg_file).absolute()
# ^ TODO to be decided by the Vectorworks API


### PROGRAM ###
dwg_to_dxf(DWG_PATH)

try:
    doc = ezdxf.readfile(DXF_PATH)                                   # some dxfs are broken, and instead needs recover.readfile(...), that's kinda scary!
    msp = doc.modelspace()
    svg = svgwrite.Drawing(filename=SVG_PATH, debug=True)
    for e in msp:
        if e.dxftype() == 'INSERT':
            convert_recursively(e.virtual_entities(), svg)
        else:
            convert_entity(e, svg)
    svg.viewbox(0, 0, 100000, 100000)                                   # TODO identify DWG document bounds and assign them here instead
    svg.save()
except IOError:
    print(f'Not a DXF file or a generic I/O error.')
    sys.exit(1)
except ezdxf.DXFStructureError:
    print(f'Invalid or corrupted DXF file.')
    sys.exit(2)
