import numpy as np
from simulator.map import Map
from simulator.objects.car import Car
from simulator.objects.wall import Wall
from simulator.physics.ray import Ray

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    car = Car("car1", np.array([15, 10]), np.array([1, 0]))
    wall1 = Wall(np.array([10, 0]), np.array([30, 0]))
    wall2 = Wall(np.array([30, 0]), np.array([30, 30]))
    game_map = Map(size=(500, 500))

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
    car.rays.append(ray1)
    car.rays.append(ray2)

    game_map.add_car(car)
    game_map.add_wall(wall1)
    game_map.add_wall(wall2)

    coll = game_map.get_cars_collisions()
    print(coll)

    game_map.generate_image()





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
