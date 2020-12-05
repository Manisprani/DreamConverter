import sys
import pathlib
import ezdxf
import svgbuilder
from convertDXF import *


debug: bool = False
input_file = "export99.dxf"


if debug:
    DEBUG_DIR = pathlib.Path(__file__).parent.joinpath('files').absolute()
    DXF_PATH = DEBUG_DIR.joinpath(input_file).absolute()
    SVG_PATH = DEBUG_DIR.joinpath(
        input_file.replace('.dxf', '.svg')).absolute()
else:
    DXF_PATH = pathlib.Path(sys.argv[1]).absolute()
    SVG_PATH = pathlib.Path(sys.argv[2]).absolute()

### PROGRAM ###
# print(DXF_PATH)
# print(SVG_PATH)
try:
    svgbuilder.build(DXF_PATH, SVG_PATH)
except IOError:
    print(f'Not a DXF file or a generic I/O error.')
    # sys.exit(1)
except ezdxf.DXFStructureError:
    print(f'Invalid or corrupted DXF file.')
    # sys.exit(2)


# vi kan ha excepts i vs-skriptet,
# och visa alert dialog om IOError
# eller DXFStructureError visas väl? :D
