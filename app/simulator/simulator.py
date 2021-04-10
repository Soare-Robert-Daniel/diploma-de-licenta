from typing import List

import numpy as np
import pandas as pd
from datetime import datetime

from simulator.generateCars import CarsGenerator
from simulator.generateWalls import WallsGenerator
from simulator.map import Map
from simulator.objects.target import Target


class Simulator:
    def __init__(self, mode="image", size=(600, 600), cars_number=1, allow_human=True):
        self.sim_map = Map(size)

        self.wall_generator = WallsGenerator(map_size=self.sim_map.size)
        self.cars_generator = CarsGenerator(cars_number=cars_number, allow_human=allow_human)
        # target = Target(np.array([50.0, 17.0]), size=15)
        print(self.wall_generator.generate_route())

        self.sim_map.extend_walls(self.wall_generator.build_walls())
        self.sim_map.extend_cars(self.cars_generator.build())
        # self.sim_map.add_target(target)
        self.cars_collisions = self.sim_map.get_cars_collisions()
        self.history = []
        self.mode = mode

    def execute(self, actions):
        self.send_actions_to_cars(actions)
        self.set_actions_record(actions)
        self.run()

        if len(self.history) >= 8000:
            self.save_csv()

    def run(self):
        for car_id in self.sim_map.cars.keys():
            if not self.is_car_crashed(car_id):
                self.compute_movement_for_car(car_id)
        self.cars_collisions = self.sim_map.get_cars_collisions()

    def send_actions_to_cars(self, actions):
        for action in actions:
            self.apply_action_to_car(action["car_id"], action["command"])

    def is_simulation_over(self):
        crashed_cars = []
        for car_id in self.sim_map.cars.keys():
            if self.is_car_crashed(car_id):
                crashed_cars.append(True)
            else:
                crashed_cars.append(False)
        return all(crashed_cars)

    def apply_action_to_car(self, car_id: str, command):
        if command == "turn_left":
            self.sim_map.cars[car_id].turn(-1)
        elif command == "turn_right":
            self.sim_map.cars[car_id].turn(1)

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
                if info["intersect"]:
                    data_car.append(info["length"])
                    if info["kind"] == "target":
                        data_car.append(0)
                    else:
                        data_car.append(1)
                else:
                    data_car.append(-1.0)
                    data_car.append(-1)
            data.append({
                "car_id": car_id,
                "sensors_data": np.array(data_car).reshape(len(car.rays), 2)
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

    def set_actions_record(self, actions):
        sensors_data = self.get_cars_sensor_data()
        for action in actions:
            car_id = action["car_id"]
            if not self.is_car_crashed(car_id):
                for sensor_data in sensors_data:
                    if car_id == sensor_data["car_id"]:
                        self.history.append({**action, **sensor_data})

    def save_csv(self):
        time_template = "%Y_%m_%d__%H_%M_%S"
        file_name = f"simulator_data_{datetime.now().strftime(time_template)}.csv"
        export_data = {
            "car_id": [],
            "command": []
        }
        for data in self.history:

            # print(data)
            export_data["car_id"].append(data["car_id"])
            export_data["command"].append(data["command"])
            for sensor_id, sensor_value in np.ndenumerate(data["sensors_data"]):
                sensor_number, data_type = sensor_id
                if data_type == 0:
                    if f"sensor_{sensor_number}_distance" in export_data.keys():
                        export_data[f"sensor_{sensor_number}_distance"].append(sensor_value)
                    else:
                        export_data[f"sensor_{sensor_number}_distance"] = [sensor_value]
                elif data_type == 1:
                    if f"sensor_{sensor_number}_object_type" in export_data.keys():
                        export_data[f"sensor_{sensor_number}_object_type"].append(sensor_value)
                    else:
                        export_data[f"sensor_{sensor_number}_object_type"] = [sensor_value]
                else:
                    raise Exception("Tipul de date al senzorului nu corespunde!")

        self.history.clear()
        df = pd.DataFrame(export_data)
        df.to_csv(f"data\\{file_name}", index=False)
        print("Saved")

    def reset(self):
        target = Target(np.array([50.0, 17.0]), size=15)

        self.sim_map.clear()
        self.sim_map.extend_walls(self.wall_generator.build_walls())
        self.sim_map.extend_cars(self.cars_generator.build())
        self.sim_map.add_target(target)
        self.cars_collisions = self.sim_map.get_cars_collisions()
