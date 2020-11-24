import svgwrite
from ezdxf.math import OCS
import math
SCALE = 1
STROKE_WIDTH = 30


def convert_line(dxf_entity):
    ocs: OCS = dxf_entity.ocs()
    ocs_line_start = dxf_entity.dxf.start
    ocs_line_end = dxf_entity.dxf.end
    line_start = [ocs.to_wcs(ocs_line_start).x, ocs.to_wcs(ocs_line_start).y]
    line_end = [ocs.to_wcs(ocs_line_end).x, ocs.to_wcs(ocs_line_end).y]
    svg_entity = svgwrite.Drawing().line(
        start=line_start,
        end=line_end,
       # stroke="black",
        stroke_width=STROKE_WIDTH,
    )
    svg_entity.scale(SCALE)
    return svg_entity


def convert_circle(dxf_entity):
    ocs: OCS = dxf_entity.ocs()
    circle_center = dxf_entity.dxf.center
    circle_center = [ocs.to_wcs(circle_center).x, ocs.to_wcs(circle_center).y]

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
    ocs: OCS = dxf_entity.ocs()
    center = dxf_entity.dxf.center
    center = [ocs.to_wcs(center).x, ocs.to_wcs(center).y]
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
    if dxf_entity.get_mode().lower() not in ["acdb2dpolyline"]:
        return
    ocs: OCS = dxf_entity.ocs()
    ocs_points = dxf_entity.points()
    wcs_points = ocs.points_to_wcs(ocs_points)
    xy_points = []
    for p in wcs_points:
        xy_points.append([p.x, p.y])
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
    ocs: OCS = dxf_entity.ocs()
    ocs_points = dxf_entity.vertices()
    # xy->xyz för att anppassa points_to_wcs transform vector
    xyz_points = []
    for p in ocs_points:
        xyz_points.append([p[0], p[1], 0])
    points = ocs.points_to_wcs(xyz_points)
    xy_points = []
    for p in points:
        xy_points.append(p[0:2])
    svg_entity = svgwrite.Drawing().polyline(
        xy_points,
        stroke="blue",
        stroke_width=STROKE_WIDTH)
    return svg_entity


def convert_arc(dxf_entity):
    ocs: OCS = dxf_entity.ocs()
    ocs_start = dxf_entity.start_point
    ocs_end = dxf_entity.end_point
    start = [ocs.to_wcs(ocs_start).x, ocs.to_wcs(ocs_start).y]
    end = [ocs.to_wcs(ocs_end).x, ocs.to_wcs(ocs_end).y]
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
    ocs: OCS = dxf_entity.ocs()
    position = dxf_entity.dxf.insert[:-1]
    # TODO ocs (really...?) No
    content = dxf_entity.text
    svg_entity = svgwrite.Drawing().text(content, position)
    svg_entity.scale(SCALE)
    return svg_entity


def convert_recursively(entities, svg, parent=None):
    for e in entities:
        if (e.dxftype() == 'INSERT'):
            convert_recursively(e.virtual_entities(), svg)
        else:
            convert_entity(e, svg)


def convert_entity(entity, svg, parent=None):
    if entity.dxftype() == 'LINE':
        svg.add(convert_line(entity))
    if entity.dxftype() == 'CIRCLE':
        svg.add(convert_circle(entity))
    if entity.dxftype() == 'LWPOLYLINE':
        svg.add(convert_lwpolyline(entity))
    if entity.dxftype() == 'POLYLINE':
        if convert_polyline(entity) is not None:
            svg.add(convert_polyline(entity))
    if entity.dxftype() == 'ARC':
        svg.add(convert_arc(entity))
    if entity.dxftype() == 'ELLIPSE':
        svg.add(convert_ellipse(entity))
