import numpy as np

from simulator.interactive.car import CarData
from simulator.objects.wall import WallData


def rotate_car_direction(car_dir, rotation_angle):
    rotation_angle = np.deg2rad(rotation_angle)
    rotation_matrix = np.array([[np.cos(rotation_angle), -np.sin(rotation_angle)],
                                [np.sin(rotation_angle), np.cos(rotation_angle)]])
    return rotation_matrix.dot(car_dir)


def calculate_next_position_car(car: CarData):
    return car.pos + car.dir * car.speed


def calculate_ray_direction(car_dir, angle):
    return rotate_car_direction(car_dir, angle)


def ray_wall_intersection(ray, wall: WallData):
    """

    :param ray:
    :param wall:
    :return:
    """
    x1, y1, x2, y2 = wall.to_line()
    x3, y3,  x4, y4 = ray

    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if den == 0:
        return False, [], 0

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

    if u > 0 and 0 <= t <= 1:
        intersection_point = np.array([x1 + t * (x2 - x1), y1 + t * (y2 - y1)])
        return True, intersection_point, np.linalg.norm(intersection_point - [ray[0], ray[1]])
    return False, [], 0




