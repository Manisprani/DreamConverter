import pathlib
import subprocess as sp
import os, sys

### I/O ### 
# TODO remove DEBUGGING constant when releasing
inputFile = "26470A7.dwg"   
outputFile = "26470A7.json"     # this decides intermediate file format

### Constants ###
LIBREDWG_DIR = pathlib.Path(__file__).parent.joinpath('libredwg').absolute()    # this one's a keeper
INPUT_PATH = pathlib.Path(__file__).parent.joinpath('testfiles').joinpath(inputFile).absolute()     # TODO remove DEBUGGING constant when releasing
OUTPUT_PATH = pathlib.Path(__file__).parent.joinpath('testfiles').joinpath(outputFile).absolute()   # TODO remove DEBUGGING constant when releasing

### FUNCTIONS ###
def dwg_to_intermediate(input_file, output_file):   
    os.chdir(LIBREDWG_DIR)
    sp.call(['dwgread.exe', input_file, '-o', output_file], shell=True)