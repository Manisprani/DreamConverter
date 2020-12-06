import sys
import pathlib
import ezdxf
import svgbuilder
from convertDXF import *


def run(input_file: str, output_path=None, debug: bool = False):
    if output_path:
        output_path = output_path[1]

    if debug:
        DEBUG_DIR = pathlib.Path(__file__).parent.joinpath('files').absolute()
        DXF_PATH = DEBUG_DIR.joinpath(input_file).absolute()
        SVG_PATH = DEBUG_DIR.joinpath(
            input_file.replace('.dxf', '.svg')).absolute()
    else:
        DXF_PATH = pathlib.Path(input_file).absolute()
        if output_path:
            SVG_PATH = pathlib.Path(output_path).joinpath(
                DXF_PATH.name.replace('.dxf', '.svg'))
        else:
            SVG_PATH = input_file.replace('.dxf', '.svg')

    ### PROGRAM ###
    try:
        svgbuilder.build(DXF_PATH, SVG_PATH)
    except IOError:
        print(f'Not a DXF file or a generic I/O error.')
        sys.exit(1)
    except ezdxf.DXFStructureError:
        print(f'Invalid or corrupted DXF file.')
        sys.exit(2)


run('export99.dxf', None, True)

# vi kan ha excepts i vs-skriptet,
# och visa alert dialog om IOError
# eller DXFStructureError visas väl? :D
