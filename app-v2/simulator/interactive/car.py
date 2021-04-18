from typing import List, Dict, Union

import numpy as np

from simulator.utility.command import Command
from simulator.utility.transformations import rotate_car_direction, calculate_next_position_car


class CarData:
    def __init__(self, car_id: Union[str, int], position, start_angle, speed=1.0, size=3.0):
        self.car_id = car_id
        self.pos = position
        self.dir = np.array([np.cos(start_angle), np.sin(start_angle)])
        self.size: float = size
        self.speed: float = speed
        self.sensors_location: List[float] = []
        self.is_crashed = False

    def as_dict(self):
        return {
            self.car_id: self
        }

    def to_list(self):
        return [{
            "car_id": self.car_id,
            "pos": self.pos,
            "dir": self.dir,
            "size": self.size,
            "speed": self.speed,
            "sensors_location": self.sensors_location,
            "x": self.pos[0],
            "y": self.pos[1]
        }]

    def set_sensors_location(self, sensors_location):
        self.sensors_location = sensors_location

    def __str__(self):
        return f"$ Car ID: {self.car_id}, Pos: {self.pos}, Dir: {self.dir}, Speed: {self.speed}, Size: {self.size}"


class CarController:
    def __init__(self, turn_rate: float = 5):
        self.turn_rate = turn_rate
        self.cars: Dict[Union[str, int], CarData] = {}

    def apply_commands(self, commands: List[Command]):
        reports = []
        for command in commands:
            if command.type == 'change_direction':
                self.change_car_direction(command.payload["car_id"], command.payload["direction"])
            elif command.type == 'move':
                self.move_car(command.payload["car_id"])
            elif command.type == 'generate_report':
                reports.append(self.generate_report(command.payload))
            elif command.type == 'car_status':
                self.cars[command.payload["car_id"]].is_crashed = command.payload["status"]
        return reports

    def add_car(self, car: CarData):
        self.cars.update(car.as_dict())

    def add_cars(self, cars: List[CarData]):
        for car in cars:
            self.add_car(car)

    def change_car_direction(self, car_id: str, direction: str):
        if car_id in self.cars:
            car = self.cars["car_id"]
            if not car.is_crashed:
                if direction == "turn_left":
                    car.dir = rotate_car_direction(car.dir, 5)
                elif direction == "turn_right":
                    car.dir = rotate_car_direction(car.dir, -5)

    def move_car(self, car_id):
        if car_id in self.cars:
            car = self.cars["car_id"]
            if not car.is_crashed:
                car.pos = calculate_next_position_car(car)

    def car_exists(self, car_id):
        return car_id in self.cars

    def generate_report(self, payload):
        pass