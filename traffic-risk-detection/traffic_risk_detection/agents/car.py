class Car:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 1
        self.dy = 0
        self.speed = 0
        self.accelaration = 0

    def run(self):
        self.speed += self.accelaration
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def set_position(self, x, y):
        self.x = x
        self.y = y
        return self

    def set_speed(self, speed):
        self.speed = speed
        return self

    def __str__(self):
        return f"Car -> Pos: ( {self.x}, {self.y}) Speed: {self.speed} Acceleration: {self.accelaration}"

    def get_position(self):
        return (self.x, self.y)

    def get_speed(self):
        return self.speed

    def get_accelaration(self):
        return self.accelaration
