import sys, pathlib, ezdxf
import svgbuilder, log
from convertDXF import *


def run(filename):
    ### I/O ###                     # TODO to be decided by Vectorworks API
    dxf_file = filename+'.dxf'
    svg_file = filename+'.svg'

    ### Constants ###                   # TODO to be decided by the Vectorworks API
    LIBREDWG_DIR = pathlib.Path(__file__).parent.joinpath('files').absolute()
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


run('ullatestdel')

# vi kan ha excepts i vs-skriptet, 
# och visa alert dialog om IOError
#  eller DXFStructureError visas väl? :D
