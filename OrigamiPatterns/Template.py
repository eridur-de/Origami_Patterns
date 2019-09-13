#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from math import pi, sin, cos

import inkex

from Path import Path
from Pattern import Pattern


# Select name of class, inherits from Pattern
# TODO:
# 1) Implement __init__ method to get all custom options and then call Pattern's __init__
# 2) Implement generate_path_tree to define all of the desired strokes


class Template(Pattern):

    def __init__(self):
        """ Constructor
        """
        Pattern.__init__(self)  # Must be called in order to parse common options

        # save all custom parameters defined on .inx file
        self.OptionParser.add_option("-p", "--pattern",
                                     action="store", type="string",
                                     dest="pattern", default="template1",
                                     help="Origami pattern")

        self.OptionParser.add_option("", "--length",
                                     action="store", type="float",
                                     dest="length", default=10.0,
                                     help="Length of grid square")

        self.OptionParser.add_option("", "--theta",
                                     action="store", type="int",
                                     dest="theta", default=0,
                                     help="Rotation angle (degree)")

    def generate_path_tree(self):
        """ Specialized path generation for your origami pattern
        """
        # retrieve conversion factor for selected unit
        unit_factor = self.calc_unit_factor()

        # retrieve saved parameters, and apply unit factor where needed
        length = self.options.length * unit_factor
        vertex_radius = self.options.vertex_radius * unit_factor
        pattern = self.options.pattern
        theta = self.options.theta * pi / 180
        s, c = sin(theta), cos(theta)

        # create all Path instances defining strokes
        # first define its points as a list of tuples...
        mountain_h_stroke_points = [(length / 2, 0),
                                    (length / 2, length)]
        mountain_v_stroke_points = [(0, length / 2),
                                    (length, length / 2)]

        # ... and then create the Path instances, defining its type ('m' for mountain, etc...)
        mountains = [Path(mountain_h_stroke_points, 'm' if pattern == 'template1' else 'v'),
                     Path(mountain_v_stroke_points, 'm' if pattern == 'template1' else 'v')]

        # doing the same for valleys
        valley_1st_stroke_points = [(0, 0),
                                    (length, length)]
        valley_2nd_stroke_points = [(0, length),
                                    (length, 0)]
        valleys = [Path(valley_1st_stroke_points, 'v' if pattern == 'template1' else 'm'),
                   Path(valley_2nd_stroke_points, 'v' if pattern == 'template1' else 'm')]



        vertices = []
        for i in range(3):
            for j in range(3):
                vertices.append(Path(((i/2.) * length, (j/2.) * length), style='p', radius=vertex_radius))

        # multiplication is implemented as a rotation, and list_rotate implements rotation for list of Path instances
        vertices = Path.list_rotate(vertices, theta, (1 * length, 1 * length))
        mountains = Path.list_rotate(mountains, theta, (1 * length, 1 * length))
        valleys = Path.list_rotate(valleys, theta, (1 * length, 1 * length))

        # if Path constructor is called with more than two points, a single stroke connecting all of then will be
        # created. Using method generate_separated_paths, you can instead return a list of separated strokes
        # linking each two points
        # create a list for edge strokes
        edge_points = [(0 * length, 0 * length),  # top left
                       (1 * length, 0 * length),  # top right
                       (1 * length, 1 * length),  # bottom right
                       (0 * length, 1 * length)]  # bottom left

        # create path from points to be able to use the already built rotate method
        edges = Path(edge_points, 'e', closed=True)
        edges = Path.list_rotate(edges, theta, (1 * length, 1 * length))

        # division is implemented as a reflection, and list_reflect implements it for a list of Path instances
        # here's a commented example:
        # line_reflect = (0 * length, 2 * length, 1 * length, 1 * length)
        # mountains = Path.list_reflect(mountains, line_reflect)
        # valleys = Path.list_reflect(valleys, line_reflect)
        # edges = Path.list_reflect(edges, line_reflect)

        # IMPORTANT: at the end, save edge points as "self.edge_points", to simplify selection of single or multiple
        # strokes for the edge
        self.edge_points = edges.points

        # IMPORTANT: the attribute "path_tree" must be created at the end, saving all strokes
        self.path_tree = [mountains, valleys, vertices]
        # if you decide not to declare "self.edge_points", then the edge must be explicitly created in the path_tree:
        # self.path_tree = [mountains, valleys, vertices, edges]




# Main function, creates an instance of the Class and calls inkex.affect() to draw the origami on inkscape
if __name__ == '__main__':
    e = Template()  # remember to put the name of your Class here!
    e.affect()
