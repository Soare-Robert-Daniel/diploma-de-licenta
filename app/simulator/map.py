from typing import Tuple, List

from simulator.objects.target import Target
from simulator.objects.wall import Wall
from PIL import Image, ImageDraw


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

    def add_wall(self, wall: Wall):
        self.walls.append(wall)

    def add_target(self, target: Target):
        self.targets.append(target)

    def add_car(self, car):
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

        for wall in self.walls:
            pos = wall.get_draw_info()
            pen.line(pos)

        for target in self.targets:
            pos = target.get_draw_info()
            pen.ellipse(pos, outline="#0000ff")

        img.show()

    def __str__(self):
        return f"#Map - Size: {self.size} - Delta Time: {self.delta_time}"
