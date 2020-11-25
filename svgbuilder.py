import re
import svgwrite
import ezdxf
from svgwrite.container import SVG
from convertDXF import *

TYPES = ["conveyor", "drop", "motor", "encoder", "estop", "photoeye", "clst"]

def build(input, output):
    doc = ezdxf.readfile(input)
    msp = doc.modelspace()
    maxPosition = (doc.header['$EXTMAX'])
    minPosition = (doc.header['$EXTMIN'])  # finds the bounds of the dxf

    svg = svgwrite.Drawing(filename=output, debug=False, transform="scale(1,-1)")
    for e in msp:
        if e.dxftype() == 'INSERT':
            # if not e.dxf.name.startswith('$'):
            #     continue
            # name_parts = re.split('-', e.dxf.name)
            # print(e.dxf.name)

            svg_group = svg.add(svg.g(
                id=e.dxf.name,
                code=e.get_attrib_text("BMK", "None"),
                type=e.get_attrib_text("TEXT1", "None"),
                stroke="black"
            ))

            convert_recursively(e.virtual_entities(), svg_group)
        else:
            convert_entity(e, svg)
    svg.viewbox(minPosition[0], minPosition[1], maxPosition[0] + \
                abs(minPosition[0]), maxPosition[1] + abs(minPosition[1]))
    svg.save()
