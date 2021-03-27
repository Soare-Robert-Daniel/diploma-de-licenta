import numpy as np

from simulator.objects.target import Target
from simulator.objects.wall import Wall


class Ray:
    def __init__(self, ray_start, ray_dir_angle):
        self.start = np.copy(ray_start)
        self.angle = np.deg2rad(ray_dir_angle)
        self.dir = np.array([np.cos(self.angle), np.sin(self.angle)])
        self.rotation_matrix = np.array([[np.cos(self.angle), -np.sin(self.angle)],
                                         [np.sin(self.angle),  np.cos(self.angle)]])

    def get_intersection_with_wall(self, wall: Wall):
        info = {
            "intersect": False
        }
        x1, y1, x2, y2 = wall.get_line()
        x3, y3 = self.start
        x4, y4 = self.start + self.dir

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if den == 0:
            return info

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        print(f"    Ray Wall Coll => Angle: {np.rad2deg(self.angle)} - t: {t} - u: {u}")

        if u > 0 and 0 < t < 1:
            info["intersect"] = True
            info["kind"] = wall.get_kind()
            info["point"] = np.array([x1 + t * (x2 - x1), y1 + t * (y2 - y1)])
            info["length"] = np.linalg.norm(info["point"] - self.start)

        return info

    def get_intersection_with_target(self, target: Target):
        # https://math.stackexchange.com/questions/311921/get-location-of-vector-circle-intersection
        info = {
            "intersect": False
        }
        x0, y0 = self.start
        x1, y1 = self.start + self.dir
        h, k = target.pos
        r = target.size / 2

        a = (x1 - x0) ** 2 + (y1 - y0) ** 2
        b = 2 * (x1 - x0) * (x0 - h) + 2 * (y1 - y0) * (y0 - k)
        c = (x0 - h) ** 2 + (y0 - k) ** 2 - r ** 2

        discriminant = b ** 2 - 4 * a * c

        if discriminant < 0:
            return info

        t1 = (-b + np.sqrt(discriminant)) / (2 * a)
        t2 = (-b - np.sqrt(discriminant)) / (2 * a)

        print(f"    ------>  t1: {t1} - t2: {t2}")

        t = np.min([t1, t2])

        if t > 0:
            info["intersect"] = True
            info["kind"] = target.get_kind()
            info["point"] = np.array([x0 + t * (x1 - x0), y1 + t * (y1 - y0)])
            info["length"] = np.linalg.norm(self.start - target.pos) - target.size

        return info

    def updates_from_car(self, car_pos, car_direction):
        self.start = np.copy(car_pos)
        self.dir = self.rotation_matrix.dot(car_direction)

    def __str__(self):
        return f"   -> Ray - Start: {self.start} - Dir: {self.dir} - Angle: {np.rad2deg(self.angle)}"
