class Car:
    def __init__(self, car_id, car_pos, car_dir, length=1):
        self.id = car_id
        self.pos = car_pos
        self.dir = car_dir
        self.length = length

    def __str__(self):
        return f"#Car - ID: {self.id} - Pos: {self.pos} - Dir: {self.dir}"
