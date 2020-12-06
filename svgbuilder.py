import re
import svgwrite
import ezdxf
from svgwrite.container import SVG
from convertDXF import *

TYPES = {
    "RF": "conveyor",
    "X0": "drop",
    "MA": "motor",
    "BG": "encoder",
    "X1": "estop",
    "SG": "photoeye",
    "X2": "clst",
    "QB": "switch ??",
    "KF": "någoting"}


def get_code(s):
    left = '.01.'
    right = '_'
    code = s[s.index(left)+len(left):s.index(right)]
    if '-' not in code:
        if '.' in code:
            code = code.split('.')[0]
    return code


def get_type(s):
    try:
        left = '.01.'
        right = '_'
        code = s[s.index(left)+len(left):s.index(right)]
        code = re.split("[-.]", code)[-1]
        for key in TYPES.keys():
            if key in code:
                return TYPES[key]
    except:
        return ""


def build(input, output):
    doc = ezdxf.readfile(input)
    msp = doc.modelspace()
    maxPosition = (doc.header['$EXTMAX'])
    minPosition = (doc.header['$EXTMIN'])  # finds the bounds of the dxf

    svg = svgwrite.Drawing(filename=output, debug=False,
                           transform="scale(1,-1)")
    for e in msp:
        if e.dxftype() == 'INSERT':
            e_type = get_type(str(e.dxf.name))
            if e_type not in TYPES.values():
                continue
            svg_group = svg.add(svg.g(
                id=e.dxf.name,
                code=get_code(str(e.dxf.name)),
                #code=e.get_attrib_text("BMK", "None"),
                type=e_type,
                stroke="black"
            ))
            #print("id= "+e.dxf.name + "\t code= " +
                  #get_code(str(e.dxf.name))+"\t type= "+e_type)
            convert_recursively(e.virtual_entities(), svg_group)
        else:
            convert_entity(e, svg)
    svg.viewbox(minPosition[0], minPosition[1], maxPosition[0] +
                abs(minPosition[0]), maxPosition[1] + abs(minPosition[1]))
    svg.save()
