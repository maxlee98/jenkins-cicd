import io
import os
from setuptools import find_packages, setup

# Metadata of package
NAME = 'ml-model-package'
DESCRIPTION = 'Loan Prediction Model'
REQUIRES_PYTHON = '>=3.7.0'

pwd = os.path.abspath(os.path.dirname(__file__))

# Get the list of packages to be installed
def list_reqs(fname='requirements.txt'):
    with io.open(os.path.join(pwd, fname), encoding='utf-8') as f:
        return f.read().splitlines()

setup(
    name=NAME, 
    version='1.0.0', 
    description=DESCRIPTION,
    packages=find_packages(),
    package_data={'prediction_model': ['VERSION']},
    python_requires=REQUIRES_PYTHON,
    install_requires=list_reqs(),
)
