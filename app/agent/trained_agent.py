from tensorflow import keras
import numpy as np

class TrainedAgent:
    def __init__(self, path_to_model):
        self.model = keras.models.load_model(path_to_model)

    def predict_command(self, sensor_data) -> str:
        # print(sensor_data)
        # np.array([sensor_data["route_completion"]])
        data = np.concatenate((np.array([sensor_data["route_completion"]]), sensor_data["sensors_data"].flatten()), axis=0)
        # print(data.shape)
        # print(np.atleast_2d(data).shape)
        predicted_values = np.argmax(self.model.predict(np.atleast_2d(data))[0])
        # print(np.array([sensor_data]).shape)
        print(f"-------> Predicted Value: {predicted_values}")
        if predicted_values == 1:
            return 'turn_right'
        elif predicted_values == 0:
            return 'turn_left'
        return 'keep_direction'
