import pyglet

from simulator.simulator import Simulator


class GameSimulator(pyglet.window.Window):
    def __init__(self, size=(600, 600), _simulator: Simulator = None):
        super(GameSimulator, self).__init__()
        self.simulator = _simulator
        self.set_size(*size)
        self.current_command = "keep_direction"

        self.label_command = pyglet.text.Label(f"Current Command: {self.current_command}", x=10, y=10,
                                               color=(243, 255, 198, 255))
        self.label_history = pyglet.text.Label(f"Saved records: {len(self.simulator.history)}/5000", x=590, y=10,
                                               anchor_x='right')

    def on_draw(self):
        self.clear()

        self.draw_simulator_objects()

        self.label_command.text = f"Current Command: {self.current_command}"
        self.label_history.text = f"Saved records: {len(self.simulator.history)}/5000"
        self.label_command.draw()
        self.label_history.draw()

    def update(self):
        if not self.simulator.is_simulation_over():
            car = self.simulator.get_cars_sensor_data()[0]
            self.simulator.execute([{"car_id": car["car_id"], "command": self.current_command}])

    def run(self):
        if self.simulator is not None:
            return lambda _: self.update()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.Q or symbol == pyglet.window.key.LEFT:
            self.current_command = "turn_right"
        elif symbol == pyglet.window.key.W or symbol == pyglet.window.key.UP:
            self.current_command = "keep_direction"
        elif symbol == pyglet.window.key.E or symbol == pyglet.window.key.RIGHT:
            self.current_command = "turn_left"
        # car = self.simulator.get_cars_sensor_data()[0]
        # if symbol == pyglet.window.key.S or symbol == pyglet.window.key.DOWN:
        #     self.simulator.send_actions_to_cars([{"car_id": car["car_id"], "command": "turn_left"}])
        # elif symbol == pyglet.window.key.W or symbol == pyglet.window.key.UP:
        #     self.simulator.send_actions_to_cars([{"car_id": car["car_id"], "command": "turn_right"}])

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
    keys = pyglet.window.key.KeyStateHandler()
    window.push_handlers(keys)

    pyglet.clock.schedule_interval(window.run(), 1 / 120.0)
    pyglet.app.run()
