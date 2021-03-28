from simulator.generateCars import CarsGenerator
from simulator.generateWalls import WallsGenerator
from simulator.map import Map
from simulator.objects.target import Target
import numpy as np


class Simulator:
    def __init__(self):
        self.sim_map = Map(size=(150, 150))

        wall_generator = WallsGenerator(map_size=self.sim_map.size)
        cars_generator = CarsGenerator()
        target = Target(np.array([50.0, 17.0]), size=15)

        self.sim_map.extend_walls(wall_generator.build_walls())
        self.sim_map.extend_cars(cars_generator.build())
        self.sim_map.add_target(target)
        self.cars_collisions = self.sim_map.get_cars_collisions()

    def run(self):
        for car_id in self.sim_map.cars.keys():
            self.compute_movement_for_car(car_id)
        self.cars_collisions = self.sim_map.get_cars_collisions()

    def send_actions_to_cars(self, actions):
        for action in actions:
            self.apply_action_to_car(action["car_id"], action["command"])

    def apply_action_to_car(self, car_id: str, command):
        if command == "turn_left":
            self.sim_map.cars[car_id].turn(-30)
        elif command == "turn_right":
            self.sim_map.cars[car_id].turn(30)

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

    def render(self):
        self.sim_map.generate_image()
