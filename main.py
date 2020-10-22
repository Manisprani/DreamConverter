from libredwg import *
import ezdxf    # if using dxf as intermediate
import json     # if using json as intermediate
import pathlib
import subprocess
import os, sys

### I/O ###
# TODO remove DEBUGGING constant when releasing
inputFile = "export99.dwg"
outputFile = "export99.json"  # this decides intermediate file format using dwg_read

### Constants ###
LIBREDWG_DIR = pathlib.Path(__file__).parent.joinpath('libredwg').absolute()    # this one's a keeper
INPUT_PATH = LIBREDWG_DIR.joinpath(inputFile).absolute()     # TODO remove DEBUGGING constant when releasing
OUTPUT_PATH = LIBREDWG_DIR.joinpath(outputFile).absolute()  # TODO remove DEBUGGING constant when releasing

### Methods ###
def print_entity(e):
    print("LINE on layer: %s\n" % e.dxf.layer)
    print("start point: %s\n" % e.dxf.start)
    print("end point: %s\n" % e.dxf.end)


#dwg_to_dxf(INPUT_PATH)
dwg_read(INPUT_PATH, OUTPUT_PATH)


