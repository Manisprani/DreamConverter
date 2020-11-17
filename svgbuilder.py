import svgwrite
import ezdxf
from convertDXF import *

def build(input, output):
    doc = ezdxf.readfile(input)
    msp = doc.modelspace()
    maxPosition = (doc.header['$EXTMAX'])
    minPosition = (doc.header['$EXTMIN'])  # finds the bounds of the dxf

    svg = svgwrite.Drawing(filename=output, debug=True)
    for e in msp:
        if e.dxftype() == 'INSERT':
            convert_recursively(e.virtual_entities(), svg)
        else:
            convert_entity(e, svg)
    svg.viewbox(minPosition[0], minPosition[1], maxPosition[0] + \
                abs(minPosition[0]), maxPosition[1] + abs(minPosition[1]))
    svg.save()