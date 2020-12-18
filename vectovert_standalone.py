from tkinter import *
from tkinter import filedialog
import main

Tk().withdraw()
dxf = filedialog.askopenfilename(filetypes=[('DXF files','.dxf')])
svg = filedialog.asksaveasfilename(filetypes=[('SVG files', '.svg')], defaultextension=".svg")

main.run(dxf, svg, False)
