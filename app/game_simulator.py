import pyglet

from agent.trained_agent import TrainedAgent
from simulator.simulator import Simulator

import tensorflow as tf

physical_devices = tf.config.list_physical_devices('GPU')
for device in physical_devices:
    tf.config.experimental.set_memory_growth(device, True)


class GameSimulator(pyglet.window.Window):
    def __init__(self, size=(600, 600), _simulator: Simulator = None):
        super(GameSimulator, self).__init__()
        self.simulator = _simulator
        self.set_size(*size)

        self.available_cars = list(filter(lambda car_id: car_id != "player",
                                          [car["car_id"] for car in self.simulator.get_cars_sensor_data()]))

        self.current_command = "keep_direction"
        self.label_command = pyglet.text.Label(f"Current Command: {self.current_command}", x=10, y=10,
                                               color=(243, 255, 198, 255))

        self.route_completion = pyglet.text.Label(f"Completion: 12.4%", x=265, y=10,
                                                  color=(180, 100, 198, 255))
        self.label_history = pyglet.text.Label(f"Saved records: {len(self.simulator.history)}/5000", font_size=11, x=590, y=10,
                                               anchor_x='right')

        self.agents = []

    def on_draw(self):
        self.clear()

        self.draw_simulator_objects()

        self.label_command.text = f"Current Command: {self.current_command}"
        self.label_history.text = f"Saved records: {len(self.simulator.history)}/8000"

        if self.simulator.allow_human:
            self.route_completion.text = f"Completion: {round( 100.0 * self.simulator.get_human_player().check_route_completion() , 2)}% "

        self.label_command.draw()
        self.label_history.draw()
        self.route_completion.draw()

    def update(self):
        if not self.simulator.is_simulation_over():
            # car = self.simulator.get_cars_sensor_data()[0]
            commands = self.get_commands_from_agents()
            if self.simulator.allow_human:
                commands.append({"car_id": "player", "command": self.current_command})
            self.simulator.execute(commands)

    def run(self):
        if self.simulator is not None:
            return lambda _: self.update()

    def get_commands_from_agents(self):
        commands = []
        for data_sensor in self.simulator.get_cars_sensor_data():
            for agent in self.agents:
                if data_sensor['car_id'] == agent['car_id']:
                    commands.append({
                        "car_id": agent["car_id"],
                        "command": agent["agent"].predict_command(data_sensor)
                    })
        return commands

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

    def assign_car_to_agent(self, agent):
        if len(self.available_cars) > 0:
            self.agents.append({
                "car_id": self.available_cars.pop(),
                "agent": agent
            })


if __name__ == '__main__':
    simulator = Simulator(mode="pyglet", cars_number=1, allow_human=True)
    window = GameSimulator(size=(600, 600), _simulator=simulator)
    keys = pyglet.window.key.KeyStateHandler()
    window.push_handlers(keys)

    trained_agent = TrainedAgent('models/test-1')
    window.assign_car_to_agent(agent=trained_agent)

    pyglet.clock.schedule_interval(window.run(), 1 / 160.0)
    pyglet.app.run()
