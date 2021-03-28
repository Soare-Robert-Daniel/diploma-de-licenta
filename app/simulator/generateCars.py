from typing import List

from simulator.objects.car import Car
import numpy as np

from simulator.physics.ray import Ray


class CarsGenerator:
    def __init__(self, cars_number=1):
        self.cars_number = cars_number

    def build(self) -> List[Car]:
        cars = []
        for car_id in range(1, self.cars_number + 1):
            car = Car(f"car_{car_id}",  np.array([15.0, 10.0]), np.array([1.0, 0]))
            spawn_angle = 45
            for a in range(360 // spawn_angle):
                ray = Ray(np.array([15, 10]), a * spawn_angle)
                car.rays.append(ray)
            cars.append(car)
        return cars

    def __str__(self):
        return f"=> Cars Generator - Walls: {self.cars_number}"
