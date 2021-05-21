from typing import Union, Dict, List

from simulator.interactive.car import CarData
from simulator.utility.collision import CollisionData
from simulator.utility.command import Command
from simulator.utility.transformations import calculate_ray_direction, ray_wall_intersection


class WallData:
    def __init__(self, wall_id: Union[str, int], start_point, end_point, sector: int = 0):
        self.start = start_point
        self.end = end_point
        self.kind = "wall"
        self.sector = sector
        self.wall_id = wall_id

    def to_list(self):
        return [{
            "wall_id": self.wall_id,
            "start": self.start,
            "end": self.end,
            "kind": self.kind,
            "sector": self.sector
        }]

    def as_dict(self):
        return {
            self.wall_id: self
        }

    def to_line(self):
        return [self.start[0], self.start[1], self.end[0], self.end[1]]

    def __str__(self):
        return f"|| Wall Id: {self.wall_id} Start: {self.start}, End: {self.end}, Sector: {self.sector}"


class WallController:
    def __init__(self):
        self.walls: Dict[Union[str, int], WallData] = {}

    def apply_commands(self, commands: List[Command]) -> List[Command]:
        reports: List[Command] = []
        for command in commands:
            if command.type == 'calculate_collisions_car':
                reports.append(self.calculate_car_collisions(command.payload["car"]))
            elif command.type == 'generate_walls':
                self.generate_walls()

        return reports

    def calculate_car_collisions(self, car: CarData) -> Command:
        def create_ray(angle):
            return [*car.pos, *(car.pos + calculate_ray_direction(car.dir, angle))]

        rays = [create_ray(sensor) for sensor in car.sensors_location]

        collisions: List[CollisionData] = []

        for sensor_id, ray in enumerate(rays):
            hits: List[CollisionData] = []
            for wall in self.walls.values():
                was_hit, point, dist = ray_wall_intersection(ray, wall)
                if was_hit:
                    hits.append(CollisionData(sensor_id, point, dist, wall.kind, wall.sector))
            collisions.append(min(hits))

        data = {
            "car_id": car.car_id,
            "sensors_data": collisions
        }
        return Command(command_type="car_collision", payload=data)

    def generate_walls(self):
        pass