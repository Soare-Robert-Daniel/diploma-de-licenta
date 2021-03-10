import matplotlib.pyplot as plt

from agents.car import Car

car1 = Car().set_position(0, 10).set_speed(0.3)

xs = []
ys = []

for i in range(30):
    car1.run()
    (x, y) = car1.get_position()
    xs.append(x)
    ys.append(y)

plt.scatter(xs, ys)
