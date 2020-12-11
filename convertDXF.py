import svgwrite
import sys
from ezdxf.math import OCS
SCALE = 1
STROKE_WIDTH = 20


def convert_line(dxf_entity, extValues=None):
    ocs: OCS = dxf_entity.ocs()
    ocs_line_start = dxf_entity.dxf.start
    ocs_line_end = dxf_entity.dxf.end
    line_start = [ocs.to_wcs(ocs_line_start).x, ocs.to_wcs(ocs_line_start).y]
    line_end = [ocs.to_wcs(ocs_line_end).x, ocs.to_wcs(ocs_line_end).y]
    if extValues:
        extValues.update(line_start)
        extValues.update(line_end)
    else:
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
        # stroke="black",
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
        # stroke="red",
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
            # stroke="green",
            stroke_width=STROKE_WIDTH)
    else:
        svg_entity = svgwrite.Drawing().polyline(
            xy_points,
            fill="none",
            # stroke="green",
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
        # stroke="blue",
        stroke_width=STROKE_WIDTH)
    return svg_entity


def convert_arc(dxf_entity, extValues=None):
    ocs: OCS = dxf_entity.ocs()
    ocs_start = dxf_entity.start_point
    ocs_end = dxf_entity.end_point
    start = [ocs.to_wcs(ocs_start).x, ocs.to_wcs(ocs_start).y]
    end = [ocs.to_wcs(ocs_end).x, ocs.to_wcs(ocs_end).y]
    if extValues:
        extValues.push_arc_start_point(start)
        extValues.push_arc_end_point(end)
    r = dxf_entity.dxf.radius
    svg_entity = svgwrite.Drawing().path(
        d=("M", start[0], start[1],
            'A', r, r,  0, 0, 1,
            end[0], end[1]),
        fill_opacity="0.0",
        stroke_width=STROKE_WIDTH,
        # stroke='grey'
    )
    return svg_entity


def convert_conveyor_block(dxf_entity, svg_group, svg):

    v = Extra_Value()
    convert_recursively(dxf_entity.virtual_entities(),
                        svg_group, svg, v)
    # close the graphic elements
    # if conveyor block has arcs, link with the arcs start points and end points
    if len(v.get_arc_start_points()) > 0:
        arc_start_points = v.get_arc_start_points()
        path1 = svgwrite.Drawing().path(
            d=("M", arc_start_points[0][0], arc_start_points[0][1]),
            stroke="black",
            stroke_width=STROKE_WIDTH,
            fill="none")
        for i in range(1, len(arc_start_points)):
            path1.push(
                "L", arc_start_points[i][0], arc_start_points[i][1])
        svg_group.add(path1)

        arc_end_points = v.get_arc_end_points()
        path2 = svgwrite.Drawing().path(
            d=("M", arc_end_points[0][0], arc_end_points[0][1]),
            # stroke="black",
            stroke_width=STROKE_WIDTH,
            fill="none")
        for i in range(1, len(arc_end_points)):
            path2.push(
                "L", arc_end_points[i][0], arc_end_points[i][1])
        svg_group.add(path2)

    # if no arcs, link the blocks corners
    else:
        vertexs = v.get_extrempoints()
        path = svgwrite.Drawing().path(
            d=("M", vertexs[3][0], vertexs[3][1]),
            # stroke="black",
            stroke_width=STROKE_WIDTH,
            fill="none")
        for vt in vertexs:
            path.push("L", vt[0], vt[1])
        svg_group.add(path)


def convert_recursively(entities, svg, parent=None, extValues=None):
    for e in entities:
        if (e.dxftype() == 'INSERT'):
            convert_recursively(e.virtual_entities(), svg, parent, extValues)
        else:
            convert_entity(e, svg, parent, extValues)


def convert_entity(entity, svg, parent=None, extValues=None):
    if entity.dxftype() == 'LINE':
        if convert_line(entity, extValues) is not None:
            svg.add(convert_line(entity, extValues))
    if entity.dxftype() == 'CIRCLE':
        svg.add(convert_circle(entity))
    if entity.dxftype() == 'LWPOLYLINE':
        svg.add(convert_lwpolyline(entity))
    if entity.dxftype() == 'POLYLINE':
        if convert_polyline(entity) is not None:
            svg.add(convert_polyline(entity))
    if entity.dxftype() == 'ARC':
        svg.add(convert_arc(entity, extValues))
    if entity.dxftype() == 'ELLIPSE':
        svg.add(convert_ellipse(entity))


class Extra_Value:
    '''record the maximum and minimum value of x and y
       collect arcs start and end points'''

    def __init__(self):
        self.minx = sys.float_info.max
        self.miny = sys.float_info.max
        self.maxx = sys.float_info.min
        self.maxy = sys.float_info.min
        self.arc_start_points = []
        self.arc_end_points = []

    def update(self, point):
        self.minx = min(self.minx, point[0])
        self.miny = min(self.miny, point[1])
        self.maxx = max(self.maxx, point[0])
        self.maxy = max(self.maxy, point[1])

    def get_extrempoints(self):
        leftUp = [self.minx, self.maxy]
        leftDown = [self.minx, self.miny]
        rightUp = [self.maxx, self.maxy]
        rightDown = [self.maxx, self.miny]
        points = [leftUp, leftDown, rightDown, rightUp]
        return points

    def push_arc_start_point(self, point):
        self.arc_start_points.append(point)

    def push_arc_end_point(self, point):
        self.arc_end_points.append(point)

    def get_arc_start_points(self):
        return self.arc_start_points

    def get_arc_end_points(self):
        return self.arc_end_points
