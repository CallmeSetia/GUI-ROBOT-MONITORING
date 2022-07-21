
import requests
import numpy as np

class Robot():
    def get_position(self, mean=0.0, standard_dev=0.1):
        # Random sensor data
        return np.random.normal(mean, standard_dev, 1)[0]

    def get_feedbackRobot(self):
        global DATA_MOTOR, ARAH_MOTOR
        try:
            url = 'http://10.42.0.1:5000'
            resp = requests.get(url=url)
            data = resp.json()  # Check the JSON
            DATA_MOTOR = data
            print("JSON", data)
            for i, data in enumerate(DATA_MOTOR):
                if data < 0:
                    ARAH_MOTOR[i] = "KIRI"
                elif data > 0:
                    ARAH_MOTOR[i] = "KANAN"
                elif data == 0:
                    ARAH_MOTOR[i] = "STOP"

        except:
            DATA_MOTOR = [0, 0, 0, 0]
        return DATA_MOTOR
