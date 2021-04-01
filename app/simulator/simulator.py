from typing import List

import numpy as np

from simulator.generateCars import CarsGenerator
from simulator.generateWalls import WallsGenerator
from simulator.map import Map
from simulator.objects.target import Target


class Simulator:
    def __init__(self, mode="image", size=(600, 600)):
        self.sim_map = Map(size)

        self.wall_generator = WallsGenerator(map_size=self.sim_map.size)
        self.cars_generator = CarsGenerator(cars_number=1)
        target = Target(np.array([50.0, 17.0]), size=15)

        self.sim_map.extend_walls(self.wall_generator.build_walls())
        self.sim_map.extend_cars(self.cars_generator.build())
        self.sim_map.add_target(target)
        self.cars_collisions = self.sim_map.get_cars_collisions()
        self.mode = mode

    def run(self):
        for car_id in self.sim_map.cars.keys():
            if not self.is_car_crashed(car_id):
                self.compute_movement_for_car(car_id)
        self.cars_collisions = self.sim_map.get_cars_collisions()

    def send_actions_to_cars(self, actions):
        for action in actions:
            self.apply_action_to_car(action["car_id"], action["command"])

    def apply_action_to_car(self, car_id: str, command):
        if command == "turn_left":
            self.sim_map.cars[car_id].turn(-5)
        elif command == "turn_right":
            self.sim_map.cars[car_id].turn(5)

    def compute_movement_for_car(self, car_id: str):
        car = self.sim_map.cars[car_id]
        new_car_pos = car.pos + car.dir * car.speed
        car.move_to(new_car_pos)

    def is_car_crashed(self, car_id: str) -> bool:
        collision = self.cars_collisions[car_id]
        for data in collision:
            if data["intersect"]:
                if data["kind"] == "wall":
                    if data["length"] <= 0:
                        return True
        return False

    def is_car_on_target(self, car_id: str) -> bool:
        collision = self.cars_collisions[car_id]
        for data in collision:
            if data["intersect"]:
                if data["kind"] == "target":
                    if data["length"] <= 0:
                        return True
        return False

    def get_cars_sensor_data(self):
        data = []
        for car_id, car in self.sim_map.cars.items():
            collision = self.cars_collisions[car_id]
            data_car = []
            for info in collision:
                data_car.append(info["length"])
                if info["kind"] == "target":
                    data_car.append(0)
                else:
                    data_car.append(1)
            data.append({
                "car_id": car_id,
                "sensor_data": np.array(data_car).reshape(len(car.rays), 2)
            })
        return data

    def get_crashed_cars(self) -> List[str]:
        crashed_cars = []
        for car_id in self.sim_map.cars.keys():
            if self.is_car_crashed(car_id):
                crashed_cars.append(car_id)
        return crashed_cars

    def get_on_target_cars(self) -> List[str]:
        on_target = []
        for car_id in self.sim_map.cars.keys():
            if self.is_car_on_target(car_id):
                on_target.append(car_id)
        return on_target

    def render(self, mode):
        if self.mode == "image" or mode == "image":
            self.sim_map.generate_image()
        elif self.mode == "pyglet" or mode == "pyglet":
            return self.sim_map.generate_pyglet_data()

    def reset(self):
        target = Target(np.array([50.0, 17.0]), size=15)

        self.sim_map.clear()
        self.sim_map.extend_walls(self.wall_generator.build_walls())
        self.sim_map.extend_cars(self.cars_generator.build())
        self.sim_map.add_target(target)
        self.cars_collisions = self.sim_map.get_cars_collisions()
