from tkinter import *
from tkinter import filedialog
import main

dxf = filedialog.askopenfilename()
svg = filedialog.asksaveasfilename()

main.run(dxf, svg, False)