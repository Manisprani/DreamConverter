import subprocess, os, pathlib

LIBREDWG_PATH = pathlib.Path(__file__).parent.joinpath('libredwg').absolute()

### FUNCTIONS ###
def dwg_to_dxf(input_file):
    os.chdir(LIBREDWG_PATH)
    subprocess.call(['dwg2dxf.exe', '-r2004', '-m', input_file, '-y'], shell=True)

def dwg_read(input_file, output_file):
    os.chdir(LIBREDWG_PATH)
    subprocess.call(['dwgread.exe', input_file, '-o', output_file, '-v0'], shell=True)