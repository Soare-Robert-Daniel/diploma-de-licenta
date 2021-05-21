from typing import List

import numpy as np

from simulator.objects.car import Car
from simulator.physics.ray import Ray


def build_ray_angles(start: float, end: float, n: int):
    return np.linspace(start=start, stop=end, num=n)


class CarsGenerator:
    def __init__(self, cars_number=1, rays_number=16, map_size=(600, 600), route=None, allow_human=True):
        if route is None:
            route = []
        self.cars_number = cars_number
        self.rays_number = rays_number
        self.map_size = map_size
        self.allow_human = allow_human
        self.cars_route = route

    def build(self) -> List[Car]:
        cars = []
        start_dir_angle = np.zeros(
            self.cars_number + 1)  # np.random.randint(low=0, high=360, size=self.cars_number + 1)
        for car_number in range(1, self.cars_number + 1):
            car = Car(car_id=f"car_{car_number}", car_pos=np.array([self.map_size[0] * 0.20, self.map_size[1] * 0.15]),
                      car_dir=np.array([np.cos(start_dir_angle[car_number]), np.sin(start_dir_angle[car_number])]))

            for a in build_ray_angles(-60, 60, self.rays_number):
                ray = Ray(np.array([self.map_size[0] * 0.10, self.map_size[1] * 0.10]), a)
                car.rays.append(ray)
            car.set_route_to_complete(self.cars_route)
            cars.append(car)

        if self.allow_human and len(cars) > 0:
            cars[0].set_id('player')

        return cars

    def __str__(self):
        return f"=> Cars Generator - Walls: {self.cars_number}"
