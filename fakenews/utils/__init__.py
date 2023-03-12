import yaml
from fakenews.exception import FakeNewsException
from fakenews.logger import logging
import sys,os
import numpy as np
import dill


def read_yaml_file(file_path: str) -> dict:
    """_summary_
    Args:
        file_path (str): file path
    Raises:
        SensorException
    Returns:
        dict: dictionary representation
              of yaml file
    """
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise SensorException(e, sys) 