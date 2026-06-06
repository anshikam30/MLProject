import yaml
import os
import sys
from src.exception import NetworkSecurityException
from src.logger import logging
import dill
import pickle


def read_yaml_file(file_path: str) -> dict:
    try: 
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)