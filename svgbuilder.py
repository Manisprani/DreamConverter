import re
import svgwrite
import ezdxf
from svgwrite.container import SVG
from convertDXF import *
#from parsing_convention import *
from NO_COMMIT_parsing_convention import *


def get_code(s):
    left = '.01.'
    right = '_'
    print(s)
    code = s[s.index(left)+len(left):s.index(right)]
    if COMPONENT_DIVIDER not in code:
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
        return ["", False]


def build(input, output):
    doc = ezdxf.readfile(input)
    msp = doc.modelspace()
    maxPosition = (doc.header['$EXTMAX'])
    minPosition = (doc.header['$EXTMIN'])  # finds the bounds of the dxf

    svg = svgwrite.Drawing(filename=output, debug=False,
                           transform="scale(1,-1)")
    for e in msp:
        if e.dxftype() == 'INSERT':
            if not e.dxf.name.startswith(CONVERSION_MARKER): continue

            res = get_type(str(e.dxf.name))
            if res is None: continue
            e_type, draw = res

            svg_group = svg.add(svg.g(
                id=e.dxf.name,
                code=get_code(str(e.dxf.name)),
                type=e_type,
                stroke="black"
            ))
            if e_type == "conveyor":
                convert_conveyor_block(e, svg_group, svg)
            elif draw:
                convert_recursively(e.virtual_entities(), svg_group)
        else:
            convert_entity(e, svg)
    svg.viewbox(minPosition[0], minPosition[1], maxPosition[0] -
                minPosition[0], maxPosition[1] - minPosition[1])
    svg.save()
