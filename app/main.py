import numpy as np

from simulator.generateWalls import WallsGenerator
from simulator.map import Map
from simulator.objects.car import Car
from simulator.objects.target import Target
from simulator.objects.wall import Wall
from simulator.physics.ray import Ray

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    car = Car("car1", np.array([15.0, 10.0]), np.array([1.0, 0]))

    # wall1 = Wall(np.array([10, 0]), np.array([30, 0]))
    # wall2 = Wall(np.array([30, 0]), np.array([25, 30]))

    # northWall = Wall(np.array([0, 0]), np.array([150, 0]))
    # southWall = Wall(np.array([0, 150]), np.array([150, 150]))
    # eastWall = Wall(np.array([0, 0]), np.array([0, 150]))
    # westWall = Wall(np.array([150, 0]), np.array([150, 150]))

    game_map = Map(size=(150, 150))
    wall_generator = WallsGenerator(map_size=game_map.size)
    target = Target(np.array([50.0, 10.0]), size=15)
    game_map.extend_walls(wall_generator.build_walls())
    # print(len(wall_generator.build_walls()))

    # inter = ray.get_intersection(wall)

    # print(car)
    # print(wall)
    # print(game_map)
    # print(ray)
    # print(inter["intersect"])
    #
    # if inter["intersect"]:
    #     print(inter["kind"])
    #     print(inter["point"])
    ray1 = Ray(np.array([15, 10]), -90)
    ray2 = Ray(np.array([15, 10]), 0)
    ray3 = Ray(np.array([15, 10]), 45)

    spawn_angle = 45
    for a in range(360 // spawn_angle):
        ray = Ray(np.array([15, 10]), a * spawn_angle)
        car.rays.append(ray)

    for _ in range(100):
        car.move()

    # car.rays.append(ray1)
    # car.rays.append(ray2)
    # car.rays.append(ray3)

    game_map.add_car(car)
    game_map.add_target(target)
    # game_map.add_wall(wall1)
    # game_map.add_wall(wall2)

    # game_map.add_wall(northWall)
    # game_map.add_wall(southWall)
    # game_map.add_wall(eastWall)
    # game_map.add_wall(westWall)

    coll = game_map.get_cars_collisions()
    print(coll)

    game_map.generate_image()





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
