import numpy as np
from typing import List

from simulator.physics.ray import Ray
from simulator.objects.wall import Wall


class Car:
    kind = "car"

    def __init__(self, car_id, car_pos, car_dir, speed=1.0, length=10.0):
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

    def check_walls_collision(self, walls: List[Wall]):
        if len(walls) == 0:
            return []
        total_collisions = []
        for wall in walls:
            total_collisions.append(self.check_wall_collision(wall))

        close_collisions = total_collisions[0]
        for collision in total_collisions:
            for index, ray_info in enumerate(collision):
                if ray_info["intersect"] and close_collisions[index]["intersect"]:
                    if ray_info["length"] < close_collisions[index]["length"]:
                        close_collisions[index] = ray_info
                elif not close_collisions[index]["intersect"]:
                    close_collisions[index] = ray_info
        return close_collisions

    def check_wall_collision(self, wall: Wall):
        collision_data = []
        for ray in self.rays:
            # print(ray)
            collision_data.append(ray.get_intersection(wall))

        # add car length in consideration for the distance between car and the wall
        for data in collision_data:
            if data["intersect"]:
                data["length"] -= self.length

        return collision_data

    def get_draw_info(self):
        return [tuple(self.pos - self.length/2), tuple(self.pos + self.length/2)]

    def __str__(self):
        return f"#Car - ID: {self.id} - Pos: {self.pos} - Dir: {self.dir}"
