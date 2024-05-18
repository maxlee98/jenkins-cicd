import pandas as pd
import numpy as np
import joblib
from config import config
from processing.data_handling import load_dataset, load_pipeline


classification_pipeline = load_pipeline(config.MODEL_NAME)


def generate_predictions(data_input):
    data = pd.DataFrame(data_input)
    pred = classification_pipeline.predict(data[config.FEATURES]) # Predict using only the x features
    output = np.where(pred == 1, "Y", "N")
    result = {"Prediction" : output}
    return result


# def generate_predictions():
#     test_data = load_dataset(config.TEST_FILE)
#     pred = classification_pipeline.predict(test_data[config.FEATURES])
#     output = np.where(pred==1,'Y','N')
#     print(output)
#     #result = {"Predictions":output}
#     return output

if __name__=='__main__':
    generate_predictions()