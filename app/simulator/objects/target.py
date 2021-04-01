import numpy as np


class Target:
    kind = "target"

    def __init__(self, position, size=10):
        self.pos = position
        self.size = size

    # def distance_to(self, car: Car):
    #     return np.linalg.norm(self.pos - car.pos) - self.size - car.length

    def get_kind(self):
        return self.kind

    def get_draw_info(self):
        return [tuple(self.pos - self.size / 2), tuple(self.pos + self.size / 2)]

    def get_pyglet_info(self):
        return {
            "type": "circle",
            "x": self.pos[0],
            "y": self.pos[1],
            "radius": self.size,
            "color": (0, 255, 0)
        }

    def __str__(self):
        return f"#Target - Pos: {self.pos} - Size: {self.size}"
