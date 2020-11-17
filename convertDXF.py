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
    if dxf_entity.is_closed:
        svg_entity = svgwrite.Drawing().polygon(
            xy_points,
            fill="none",
            stroke="green",
            stroke_width=STROKE_WIDTH)
    else:
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


def convert_arc(dxf_entity):
    start = dxf_entity.start_point[:-1]
    end = dxf_entity.end_point[:-1]
    r = dxf_entity.dxf.radius
    svg_entity = svgwrite.Drawing().path(
        d=("M", start[0], start[1],
            'A', r, r,  0, 0, 1,
            end[0], end[1]),
        fill_opacity="0.0",
        stroke_width=STROKE_WIDTH,
        stroke='grey')
    return svg_entity


# FIXME entities are added to SVG, but they're not visible. Scale-related?
def convert_mtext(dxf_entity):
    position = dxf_entity.dxf.insert[:-1]
    print(position)
    content = dxf_entity.text
    svg_entity = svgwrite.Drawing().text(content, position)
    svg_entity.scale(SCALE)
    return svg_entity


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
    if entity.dxftype() == 'ARC':
        svg.add(convert_arc(entity))
    if entity.dxftype() == 'ELLIPSE':
        svg.add(convert_ellipse(entity))
