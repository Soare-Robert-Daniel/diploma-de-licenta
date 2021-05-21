class CollisionData:
    def __init__(self, sensor_id, point, distance, kind, sector):
        self.sensor_id = sensor_id
        self.dist = distance
        self.point = point
        self.kind = kind
        self.sector = sector

    def to_list(self):
        return [{
            "sensor_id": self.sensor_id,
            "point": self.point,
            "dist": self.dist,
            "kind": self.kind,
            "sector": self.sector
        }]

    def as_dict(self):
        return {
            "sensor_id": self
        }

    def __lt__(self, other):
        return self.dist < other.dist

    def __le__(self, other):
        return self.dist <= other.dist

    def __gt__(self, other):
        return self.dist > other.dist

    def __ge__(self, other):
        return self.dist >= other.dist

    def __eq__(self, other):
        return self.dist == other.dist

    def __ne__(self, other):
        return self.dist != other.dist
