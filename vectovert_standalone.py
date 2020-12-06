from tkinter import *
from tkinter import filedialog
import main

Tk().withdraw()
dxf = filedialog.askopenfilename()
svg = filedialog.asksaveasfilename()

main.run(dxf, svg, False)