from typing import List

from simulator.objects.wall import Wall
import numpy as np
import shapely.geometry as shp
from shapely.geometry import CAP_STYLE, JOIN_STYLE

class WallsGenerator:
    def __init__(self, walls_number=3, map_size=(150, 150)):
        self.walls_number = walls_number
        self.map_size = map_size
        self.path = np.array([[10.0, 50.0], [600.0, 50.0], [600.0, 600.0], [310.0, 310.0], [10.0, 600.0]])

    def build_walls(self) -> List[Wall]:
        map_walls = self.generate_outer_walls()
        # map_walls.extend(self.generate_inner_walls())
        map_walls.extend(self.generate_route())
        return map_walls

    def generate_outer_walls(self) -> List[Wall]:
        width, height = self.map_size
        north_wall = Wall(np.array([0, 0]), np.array([width, 0]))
        south_wall = Wall(np.array([0, height]), np.array([width, height]))
        east_wall = Wall(np.array([0, 0]), np.array([0, height]))
        west_wall = Wall(np.array([width, 0]), np.array([width, height]))

        return [north_wall, south_wall, east_wall, west_wall]

    def generate_inner_walls(self) -> List[Wall]:
        width, height = self.map_size
        # wall1 = Wall(np.array([width // 2, 30]), np.array([width // 2, height - 30]))
        # wall2 = Wall(np.array([30, height // 2]), np.array([width - 30, height // 2]))
        wall1 = Wall(np.array([int(width * 0.2), int(height * 0.2)]), np.array([width - int(width * 0.2), int(height * 0.2)]))
        wall2 = Wall(np.array([width - int(width * 0.2), int(height * 0.2)]), np.array([width - int(width * 0.2), height - int(height * 0.2)]))
        wall3 = Wall(np.array([width - int(width * 0.2), height - int(height * 0.2)]), np.array([int(width * 0.2), height - int(height * 0.2)]))
        wall4 = Wall(np.array([int(width * 0.2), height - int(height * 0.2)]), np.array([int(width * 0.2), int(height * 0.2)]))
        return [wall1, wall2, wall3, wall4]

    def generate_route(self) -> List[Wall]:
        route = shp.Polygon(self.path)
        margin = route.buffer(-80, join_style=JOIN_STYLE.round)

        walls1_points = np.array(route.exterior)
        walls2_points = np.array(margin.exterior)

        walls = []
        # walls1_points = np.append(walls1_points, [walls1_points[0]], axis=0)
        for idx in range(len(walls1_points) - 1):
            walls.append(Wall(walls1_points[idx], walls1_points[idx + 1]))
        # walls2_points = np.append(walls2_points, [walls2_points[0]], axis=0)
        for idx in range(len(walls2_points) - 1):
            walls.append(Wall(walls2_points[idx], walls2_points[idx + 1]))

        return walls

    def get_route(self):
        return np.array(shp.Polygon(self.path).exterior)

    def __str__(self):
        return f"=> Walls Generator - Walls: {self.walls_number}"
