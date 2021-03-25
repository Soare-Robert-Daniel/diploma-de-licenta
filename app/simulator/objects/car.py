import numpy as np
from typing import List

from simulator.physics.ray import Ray
from simulator.objects.wall import Wall


class Car:
    kind = "car"

    def __init__(self, car_id, car_pos, car_dir, speed=1.0, length=1.0):
        self.id: str = car_id
        self.pos = car_pos
        self.dir = car_dir
        self.length: float = length
        self.speed: float = speed
        self.rays: List[Ray] = []

    def move(self):
        self.pos += self.dir * self.speed

    def update(self, direction):
        self.dir = np.copy(direction)

    def update_rays(self):
        for ray in self.rays:
            ray.updates_from_car(self.pos, self.dir)

    def check_wall_collision(self, wall: Wall):
        collision_data = []
        for ray in self.rays:
            collision_data.append(ray.get_intersection(wall))

        # add car length in consideration for the distance between car and the wall
        for data in collision_data:
            if data["intersect"]:
                data["length"] -= self.length

        return collision_data

    def __str__(self):
        return f"#Car - ID: {self.id} - Pos: {self.pos} - Dir: {self.dir}"
