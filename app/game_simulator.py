import pyglet

from simulator.simulator import Simulator


class GameSimulator(pyglet.window.Window):
    def __init__(self, size=(600, 600), _simulator: Simulator = None):
        super(GameSimulator, self).__init__()
        self.simulator = _simulator
        self.set_size(*size)

        self.label = pyglet.text.Label('Game Simulator')

    def on_draw(self):
        self.clear()

        self.draw_simulator_objects()
        self.label.draw()

    def update(self):
        return lambda _: self.simulator.run()

    def on_key_press(self, symbol, modifiers):
        car = self.simulator.get_cars_sensor_data()[0]
        if symbol == pyglet.window.key.S:
            self.simulator.send_actions_to_cars([{"car_id": car["car_id"], "command": "turn_left"}])
        elif symbol == pyglet.window.key.W:
            self.simulator.send_actions_to_cars([{"car_id": car["car_id"], "command": "turn_right"}])

    def draw_simulator_objects(self):
        if self.simulator is not None:
            draw_date = self.simulator.render(mode="pyglet")

            for data in draw_date:
                if data["type"] == "circle":
                    pyglet.shapes.Circle(
                        x=data["x"],
                        y=data["y"],
                        radius=data["radius"],
                        color=data["color"]
                    ).draw()
                elif data["type"] == "line":
                    pyglet.shapes.Line(
                        x=data["x"],
                        y=data["y"],
                        x2=data["x2"],
                        y2=data["y2"],
                        color=data["color"],
                        width=1
                    ).draw()


if __name__ == '__main__':
    simulator = Simulator(mode="pyglet")
    window = GameSimulator(size=(600, 600), _simulator=simulator)
    pyglet.clock.schedule_interval(window.update(), 1/120.0)
    pyglet.app.run()
