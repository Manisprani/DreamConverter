import sys, pathlib, ezdxf
from libredwg import *
from ezdxf import recover
from convertDXF import *

print_to_log_file = False    # Whether print statements should print to a log.txt file, or in console.

### I/O ###                         # TODO to be decided by Vectorworks API
dwg_file = 'FILE GO HERE.dwg'       # TODO currently not used. Vectorworks API will load chosen DWG, export it to DXF, and use the exported DXF as it's intermediary file
dxf_file = 'FILE GO HERE.dxf'
svg_file = 'FILE GO HERE.svg'


### Constants ###                   # TODO to be decided by the Vectorworks API
LIBREDWG_DIR = pathlib.Path(__file__).parent.joinpath('libredwg').absolute()
DWG_PATH = LIBREDWG_DIR.joinpath(dwg_file).absolute()
DXF_PATH = LIBREDWG_DIR.joinpath(dxf_file).absolute()
SVG_PATH = LIBREDWG_DIR.joinpath(svg_file).absolute()

def print_entity(e):
    print("start point: %s\n" % e.dxf.start)
    print("end point: %s\n" % e.dxf.end)


### PROGRAM ###
if print_to_log_file:
    sys.stdout = open('log.txt', 'w')

try:
    doc = ezdxf.readfile(DXF_PATH)      # some dxfs from libredwg are broken, and instead needs recover.readfile(...), which seems to delete the INSERTs...
    msp = doc.modelspace()
    maxPosition = (doc.header['$EXTMAX'])
    minPosition = (doc.header['$EXTMIN']) # finds the bounds of the dxf
    print (doc.header['$EXTMAX'])
    print (doc.header['$EXTMIN'])

  

    svg = svgwrite.Drawing(filename=SVG_PATH, debug=True)
    for e in msp:
        if e.dxftype() == 'INSERT':
            convert_recursively(e.virtual_entities(), svg)
        else:
            convert_entity(e, svg)
    svg.viewbox(minPosition[0],minPosition[1], maxPosition[0] + abs(minPosition[0]), maxPosition[1] + abs(minPosition[1]))   
    svg.save()
except IOError:
    print(f'Not a DXF file or a generic I/O error.')
    sys.exit(1)
except ezdxf.DXFStructureError:
    print(f'Invalid or corrupted DXF file.')
    sys.exit(2)
