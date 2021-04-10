import numpy as np
from typing import List

from simulator.objects.target import Target
from simulator.physics.ray import Ray
from simulator.objects.wall import Wall


class Car:
    kind = "car"
    color = (255, 0, 0)

    def __init__(self, car_id, car_pos, car_dir, speed=1.0, length=10.0):
        self.id: str = car_id
        self.pos = car_pos
        self.dir = car_dir
        self.length: float = length
        self.speed: float = speed
        self.rays: List[Ray] = []
        self.past_pos = [np.copy(self.pos)]
        self.path = None

    def turn(self, turn_angle):
        turn_angle = np.deg2rad(turn_angle)
        rotation_matrix = np.array([[np.cos(turn_angle), -np.sin(turn_angle)],
                                    [np.sin(turn_angle), np.cos(turn_angle)]])
        self.dir = rotation_matrix.dot(self.dir)
        self.update_rays()

    def move_to(self, new_pos):
        self.pos = new_pos
        self.update_rays()
        self.past_pos.append(np.copy(self.pos))

    def update(self, direction):
        self.dir = np.copy(direction)
        self.update_rays()

    def update_rays(self):
        for ray in self.rays:
            ray.updates_from_car(self.pos, self.dir)

    def check_collision(self, walls: List[Wall], targets: List[Target]):
        if len(walls) == 0 or len(self.rays) == 0:
            return []
        total_collisions = []
        for wall in walls:
            total_collisions.append(self.check_wall_collision(wall))

        for target in targets:
            total_collisions.append(self.check_target_collision(target))

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
            collision_data.append(ray.get_intersection_with_wall(wall))

        # add car length in consideration for the distance between car and the wall
        for data in collision_data:
            if data["intersect"]:
                data["length"] -= self.length / 2

        return collision_data

    def check_target_collision(self, target: Target):
        collision_data = []
        for ray in self.rays:
            # print(ray)
            collision_data.append(ray.get_intersection_with_target(target))

        # add car length in consideration for the distance between car and the wall
        for data in collision_data:
            if data["intersect"]:
                data["length"] -= self.length / 2

        return collision_data

    def get_draw_info(self):
        return [tuple(self.pos - self.length / 2), tuple(self.pos + self.length / 2)]

    def get_pyglet_info(self):
        return {
            "type": "circle",
            "x": self.pos[0],
            "y": self.pos[1],
            "radius": self.length,
            "color": self.color
        }

    def get_pyglet_info_direction(self):
        return {
            "type": "line",
            "x": self.pos[0],
            "y": self.pos[1],
            "x2": self.pos[0] + self.dir[0] * self.length,
            "y2": self.pos[1] + self.dir[1] * self.length,
            "color": (255, 255, 255)
        }

    def get_path_draw(self):
        path = []
        if len(self.past_pos) >= 2:
            for i in range(len(self.past_pos) - 1):
                path.append([tuple(self.past_pos[i]), tuple(self.past_pos[i + 1])])
        return path

    def set_id(self, car_id):
        self.id = car_id
        if car_id == "player":
            self.color = (255, 0, 255)

    def set_path(self, path):
        self.path = path

    def __str__(self):
        return f"#Car - ID: {self.id} - Pos: {self.pos} - Dir: {self.dir}"
