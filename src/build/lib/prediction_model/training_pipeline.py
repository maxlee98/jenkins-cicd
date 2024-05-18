import pandas as pd
import numpy as np
from config import config
from processing.data_handling import load_dataset, save_pipeline
import pipeline as pipe

def perform_training():
    train_data = load_dataset(config.TRAIN_FILE)
    train_y = train_data[config.TARGET].map({'N':0, 'Y':1})
    pipe.classification_pipeline.fit(train_data[config.FEATURES], train_y)
    save_pipeline(pipe.classification_pipeline)

if __name__ == "__main__":
    perform_training()