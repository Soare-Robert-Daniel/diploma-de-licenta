
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

    def __str__(self):
        return f"#Wall - Start: {self.start} - End: {self.end}"
