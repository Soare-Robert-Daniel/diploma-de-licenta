from typing import Tuple, List

from simulator.objects.car import Car
from simulator.objects.target import Target
from simulator.objects.wall import Wall
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt


class Map:

    def __init__(self, size: Tuple[int, int], frame_rate=30):
        self.size: Tuple[int, int] = size
        self.walls: List[Wall] = []
        self.cars = {}
        self.targets = []
        self.delta_time: float = 1.0 / frame_rate

    def apply_actions_from_agents(self, actions):
        pass

    def extend_walls(self, walls: List[Wall]):
        self.walls.extend(walls)

    def extend_cars(self, cars: List[Car]):
        for car in cars:
            self.add_car(car)

    def add_wall(self, wall: Wall):
        self.walls.append(wall)

    def add_target(self, target: Target):
        self.targets.append(target)

    def add_car(self, car: Car):
        self.cars[car.id] = car

    def get_cars_collisions(self):
        cars_collisions = {}

        for car_id, car in self.cars.items():
            cars_collisions[car_id] = car.check_collision(self.walls, self.targets)

        return cars_collisions

    def generate_image(self):
        img = Image.new(mode="RGB", size=self.size, color=(209, 123, 193))
        pen = ImageDraw.Draw(img)

        for car in self.cars.values():
            pos = car.get_draw_info()
            pen.ellipse(pos, outline="#00ff00", fill="#ff0000")

            collisions = car.check_collision(self.walls, self.targets)
            for collision in collisions:
                if collision["intersect"]:
                    start_point = tuple(car.pos)
                    end_point = tuple(collision["point"])
                    pen.line([start_point, end_point], fill="#000")

            for path in car.get_path_draw():
                pen.line(path, fill="#126789")

        for wall in self.walls:
            pos = wall.get_draw_info()
            pen.line(pos)

        for target in self.targets:
            pos = target.get_draw_info()
            pen.ellipse(pos, outline="#0000ff")

        # img.show()
        plt.imshow(img)
        plt.show()

    def generate_pyglet_data(self):
        draw_data = []
        for car in self.cars.values():

            collisions = car.check_collision(self.walls, self.targets)
            for collision in collisions:
                if collision["intersect"]:
                    start_point = tuple(car.pos)
                    end_point = tuple(collision["point"])
                    draw_data.append({
                        "type": "line",
                        "x": start_point[0],
                        "y": start_point[1],
                        "x2": end_point[0],
                        "y2": end_point[1],
                        "color": (201, 105, 100)
                    })
            draw_data.append(car.get_pyglet_info())
            draw_data.append(car.get_pyglet_info_direction())
            # for path in car.get_path_draw():
            #     draw_data.append({
            #
            #     })

        for wall in self.walls:
            draw_data.append(wall.get_pyglet_info())

        for target in self.targets:
            draw_data.append(target.get_pyglet_info())

        return draw_data

    def clear(self):
        self.cars.clear()
        self.walls.clear()
        self.targets.clear()

    def __str__(self):
        return f"#Map - Size: {self.size} - Delta Time: {self.delta_time}"
