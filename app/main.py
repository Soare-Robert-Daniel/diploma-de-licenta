import numpy as np
from simulator.map import Map
from simulator.objects.car import Car
from simulator.objects.wall import Wall
from simulator.physics.ray import Ray

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    car = Car("car1", np.array([10, 10]), np.array([1, 0]))
    wall = Wall(np.array([10, 0]), np.array([30, 0]))
    game_map = Map(size=(500, 500))
    ray = Ray(np.array([15, 10]), -80)

    inter = ray.get_intersection(wall)

    print(car)
    print(wall)
    print(game_map)
    print(ray)
    print(inter["intersect"])

    if inter["intersect"]:
        print(inter["kind"])
        print(inter["point"])



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
