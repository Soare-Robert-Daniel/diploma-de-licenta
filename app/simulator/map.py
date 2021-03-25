from typing import Tuple, List
from simulator.objects.wall import Wall


class Map:

    def __init__(self, size: Tuple[int, int], frame_rate=30):
        self.size: Tuple[int, int] = size
        self.walls: List[Wall] = []
        self.cars = {}
        self.delta_time: float = 1.0 / frame_rate

    def apply_actions_from_agents(self, actions):
        pass

    def add_wall(self, wall: Wall):
        self.walls.append(wall)

    def add_car(self, car):
        self.cars[car.id] = car

    def get_car_collisions(self):
        cars_collisions = {}
        for wall in self.walls:
            for car_id, car in self.cars.items():
                cars_collisions[car_id] = car.check_wall_collision(wall)

    def __str__(self):
        return f"#Map - Size: {self.size} - Delta Time: {self.delta_time}"
