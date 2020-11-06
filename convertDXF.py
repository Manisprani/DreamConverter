import svgwrite
import math
SCALE = 1
STROKE_WIDTH = 30


def convert_line(dxf_entity):
    line_start = dxf_entity.dxf.start[:2]
    line_end = dxf_entity.dxf.end[:2]
    svg_entity = svgwrite.Drawing().line(
        start=line_start,
        end=line_end,
        stroke="black",
        stroke_width=STROKE_WIDTH,
    )
    svg_entity.scale(SCALE)
    return svg_entity


def convert_circle(dxf_entity):
    circle_center = dxf_entity.dxf.center[:2]
    circle_radius = dxf_entity.dxf.radius
    svg_entity = svgwrite.Drawing().circle(
        center=circle_center,
        r=circle_radius,
        stroke="black",
        stroke_width=STROKE_WIDTH,
        fill="none",
    )
    svg_entity.scale(SCALE)
    return svg_entity


def convert_ellipse(dxf_entity):
    center = dxf_entity.dxf.center[:2]
    major_axis = dxf_entity.dxf.major_axis
    minor_axis = dxf_entity.minor_axis
    r = [major_axis[0], minor_axis[1]]
    svg_entity = svgwrite.Drawing().ellipse(
        center=center,
        r=r,
        fill="none",
        stroke="red",
        stroke_width=STROKE_WIDTH)
    return svg_entity


def convert_polyline(dxf_entity):
    points = dxf_entity.points()
    xy_points = []
    for p in points:
        xy_points.append(p[:2])
    svg_entity = svgwrite.Drawing().polyline(
        xy_points,
        fill="none",
        stroke="green",
        stroke_width=STROKE_WIDTH)
    return svg_entity


def convert_lwpolyline(dxf_entity):
    points = dxf_entity.vertices()
    svg_entity = svgwrite.Drawing().polyline(
        points,
        stroke="blue",
        stroke_width=STROKE_WIDTH)
    return svg_entity


def convert_ARC(dxf_entity):
    center = dxf_entity.dxf.center[:2]
    radius = dxf_entity.dxf.radius
    start_angle = dxf_entity.dxf.start_angle
    end_angle = dxf_entity.dxf.end_angle
    target = [center[0] + math.cos(end_angle), center[1] + math.sin(end_angle)]
    if (abs(start_angle - end_angle) < math.pi):
        large_arc = False
    else:
        large_arc = True
    if (end_angle - start_angle > 0):
        angle_dir = '+'
    else:
        angle_dir = '-'
    svg_entity = svgwrite.Drawing().path(d=(
        "M",
        center[0] + math.cos(start_angle),
        center[1] + math.sin(start_angle),
    ),
        stroke_width=STROKE_WIDTH)
    svg_entity.push_arc(target,
                        0,
                        radius,
                        large_arc=large_arc,
                        angle_dir=angle_dir,
                        absolute=False)
    return svg_entity


def convert_polyline(dxf_entity):
    return None


def convert_recursively(entities, svg):
    for e in entities:
        if (e.dxftype() == 'INSERT'):
            convert_recursively(e.virtual_entities(), svg)
        else:
            print(e)
            convert_entity(e, svg)


def convert_entity(entity, svg):
    if entity.dxftype() == 'LINE':
        svg.add(convert_line(entity))
    if entity.dxftype() == 'CIRCLE':
        svg.add(convert_circle(entity))
    if entity.dxftype() == 'LWPOLYLINE':
        svg.add(convert_lwpolyline(entity))
    if entity.dxftype() == 'POLYLINE':
        svg.add(convert_polyline(entity))
    # if entity.dxftype() == 'ARC':
    #     svg.add(convert_ARC(entity))     # FIXME undefined behaviour
    if entity.dxftype() == 'ELLIPSE':
        svg.add(convert_ellipse(entity))
