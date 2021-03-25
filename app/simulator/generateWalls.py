class WallsGenerator:
    def __init__(self, walls_number=3):
        self.walls_number = walls_number

    def __str__(self):
        return f"=> Walls Generator - Walls: {self.walls_number}"