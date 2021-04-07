from tensorflow import keras
import numpy as np

class TrainedAgent:
    def __init__(self, path_to_model):
        self.model = keras.models.load_model(path_to_model)

    def predict_command(self, sensor_data) -> str:
        # print(sensor_data.shape)
        predicted_values = self.model.predict(x=np.array([sensor_data]))[0][0]
        # print(np.array([sensor_data]).shape)
        print(predicted_values)
        if predicted_values >= 0.3:
            return 'turn_right'
        elif predicted_values <= -0.6:
            return 'turn_left'
        return 'keep_direction'
