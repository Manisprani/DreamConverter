import sys
import ezdxf
import pathlib
import svgbuilder
from convertDXF import *

def run(input_path: str, output_path=None, debug: bool = False):
    '''
    The main method for running the conversion script. It takes two paths as parameters, so it can be adapted to an interface of choice.
    '''

    if debug:
        DEBUG_DIR = pathlib.Path(__file__).parent.joinpath('files').absolute()
        DXF_PATH = DEBUG_DIR.joinpath(input_path).absolute()
        SVG_PATH = DEBUG_DIR.joinpath(
            input_path.replace('.dxf', '.svg')).absolute()
    else:
        DXF_PATH = input_path
        SVG_PATH = output_path

    ### PROGRAM ###
    try:
        svgbuilder.build(DXF_PATH, SVG_PATH)
    except IOError:
        print(f'Not a DXF file or a generic I/O error.')
        sys.exit(1)
    except ezdxf.DXFStructureError:
        print(f'Invalid or corrupted DXF file.')
        sys.exit(2)

# excepts could also be thrown to Vectorworks!
