import numpy as np
from simulator.objects.wall import Wall


class Ray:
    def __init__(self, ray_start, ray_dir_angle):
        self.start = np.copy(ray_start)
        self.angle = np.deg2rad(ray_dir_angle)
        self.dir = np.array([np.cos(self.angle), np.sin(self.angle)])
        self.rotation_matrix = np.array([[np.cos(self.angle), -np.sin(self.angle)],
                                         [np.sin(self.angle),  np.cos(self.angle)]])

    def get_intersection(self, wall: Wall):
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

        print(f"Ray Coll => Angle: {np.rad2deg(self.angle)} - t: {t} - u: {u}")

        if u > 0 and 0 < t < 1:
            info["intersect"] = True
            info["kind"] = wall.get_kind()
            info["point"] = np.array([x1 + t * (x2 - x1), y1 + t * (y2 - y1)])
            info["length"] = np.linalg.norm(info["point"] - self.start)

        return info

    def updates_from_car(self, car_pos, car_direction):
        self.start = np.copy(car_pos)
        self.dir = self.rotation_matrix.dot(car_direction)

    def __str__(self):
        return f"   -> Ray - Start: {self.start} - Dir: {self.dir} - Angle: {np.rad2deg(self.angle)}"
