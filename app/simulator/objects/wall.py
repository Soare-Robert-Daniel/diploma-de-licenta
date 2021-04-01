
class Wall:
    kind = "wall"

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_line(self):
        x1, y1 = self.start
        x2, y2 = self.end
        return x1, y1, x2, y2

    def get_kind(self):
        return self.kind

    def get_draw_info(self):
        return [tuple(self.start), tuple(self.end)]

    def get_pyglet_info(self):
        return {
            "type": "line",
            "x": self.start[0],
            "y": self.start[1],
            "x2": self.end[0],
            "y2": self.end[1],
            "color": (0, 0, 255)
        }

    def __str__(self):
        return f"#Wall - Start: {self.start} - End: {self.end}"
