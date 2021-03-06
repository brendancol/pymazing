"""3D plane representation."""
# Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
# License: MIT, see the LICENSE file.

import numpy as np


class Plane:
    def __init__(self):
        self.normal = np.array([0.0, 0.0, 0.0])
        self.distance = 0.0

    def setup_from_points(self, p0, p1, p2):
        """
        Construct the plane from three points.
        """
        normal = np.cross(p1 - p0, p2 - p0)
        distance = -(normal[0] * p0[0] + normal[1] * p0[1] + normal[2] * p0[2])
        normal_length = np.linalg.norm(normal)
        self.normal = normal / normal_length
        self.distance = distance / normal_length

    def point_distance(self, p):
        """
        Signed distance of a point from the plane.
        """
        return np.dot(p, self.normal) + self.distance
