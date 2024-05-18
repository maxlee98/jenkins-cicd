import os 
import pandas as pd
import joblib
from prediction_model.config import config

# Load Data
def load_dataset(file_name):
    filepath = os.path.join(config.DATAPATH, file_name)
    _data = pd.read_csv(filepath)
    return _data

# Serialisation
def save_pipeline(pipeline_to_save):
    save_path = os.path.join(config.SAVE_MODEL_PATH, config.MODEL_NAME)
    joblib.dump(value=pipeline_to_save, filename=save_path)
    print(f"Model has been saved under the name {config.MODEL_NAME}")

# Deserialisation
def load_pipeline(pipeline_to_load):
    save_path = os.path.join(config.SAVE_MODEL_PATH, config.MODEL_NAME)
    model_loaded = joblib.load(filename=save_path)
    print(f"Model has been loaded under the name {config.MODEL_NAME}")
    return model_loaded
