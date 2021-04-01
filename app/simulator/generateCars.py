from typing import List

import numpy as np

from simulator.objects.car import Car
from simulator.physics.ray import Ray


class CarsGenerator:
    def __init__(self, cars_number=1, rays_number=8, map_size=(600, 600)):
        self.cars_number = cars_number
        self.rays_number = rays_number
        self.map_size = map_size

    def build(self) -> List[Car]:
        cars = []
        start_dir_angle = np.random.randint(low=0, high=360, size=self.cars_number + 1)
        for car_number in range(1, self.cars_number + 1):
            car = Car(car_id=f"car_{car_number}", car_pos=np.array([self.map_size[0] * 0.12, self.map_size[1] * 0.10]),
                      car_dir=np.array([np.cos(start_dir_angle[car_number]), np.sin(start_dir_angle[car_number])]))
            spawn_angle = 360 / self.rays_number
            for a in range(self.rays_number):
                ray = Ray(np.array([self.map_size[0] * 0.10, self.map_size[1] * 0.10]), a * spawn_angle)
                car.rays.append(ray)
            cars.append(car)
        return cars

    def __str__(self):
        return f"=> Cars Generator - Walls: {self.cars_number}"
