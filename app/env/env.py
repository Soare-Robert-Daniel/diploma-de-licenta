from simulator.simulator import Simulator


class Env:
    def __init__(self):
        self.simulator = Simulator()

    def reset(self):
        self.simulator.reset()
        return self.simulator.get_cars_sensor_data()

    def step(self, actions):

        self.simulator.send_actions_to_cars(actions)
        crashed_cars = self.simulator.get_crashed_cars()
        successful_cars = self.simulator.get_on_target_cars()

        rewards = []
        done = []

        for car_id in self.simulator.sim_map.cars:
            if car_id in crashed_cars:
                rewards.append(-100)
                done.append(True)
            elif car_id in successful_cars:
                rewards.append(100)
                done.append(True)
            else:
                rewards.append(-1)
                done.append(False)

        observations = self.simulator.get_cars_sensor_data()

        return observations, rewards, done

    def render(self):
        self.simulator.render()
