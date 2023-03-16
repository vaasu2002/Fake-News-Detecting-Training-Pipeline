import yaml
from fakenews.exception import FakeNewsException
from fakenews.logger import logging
import sys,os
import numpy as np
import dill


def save_numpy_array_data(file_path: str, array: np.array):
    """ To save numpy array data to a file
    Args:
        file_path (str): str location of file to save
        array (np.array): np.array data to save
    Raises:
        FakeNewsException
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise FakeNewsException(e, sys) from e

def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise FakeNewsException(e, sys) from e


def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise FakeNewsException(e, sys) from 