# Tests #
# output from predict script not null
# output from predict script is str data type
# the output is Y for example data

# Config #
# [pytest]
# addopts = -p no:warnings

import pytest
from prediction_model.config import config
from prediction_model.processing.data_handling import load_dataset
from prediction_model.predict import generate_predictions

# Making use of Fixtures in pytest
# Fixtures run before each test function

@pytest.fixture #this res is needed for all tests
def single_prediction():
    test_dataset = load_dataset(config.TEST_FILE)
    single_row = test_dataset[:1]
    res = generate_predictions(single_row)
    print(res) # result = {"Prediction" : output}
    return res

def test_single_pred_not_none(single_prediction): # output not none
    assert single_prediction is not None

def test_single_pred_str_type(single_prediction): # output is string
    assert isinstance(single_prediction['Prediction'][0], str)

def test_single_pred_validate(single_prediction):
    assert single_prediction['Prediction'][0] == 'Y'
