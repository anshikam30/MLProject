import yaml
import os
import sys
from src.exception import NetworkSecurityException
from src.logger import logging
import dill
import pickle
import numpy as np

def read_yaml_file(file_path: str) -> dict:
    try: 
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def write_yaml_file(file_path: str , content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path): os.remove(file_path)
            
        os.makedirs(os.path.dirname(file_path), exist_ok= True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def save_numpy_array(array : np.array, path:str):
    try:
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path, exist_ok=True)
        with open(path,"wb") as file:
            np.save(file, array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
    
def load_numpy_array(path:str):
    try:
        with open(path,"rb") as file:
            return np.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def save_object(path: str, obj):
    try:
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path, exist_ok=True)
        with open(path,"wb") as file:
            pickle.dump(obj, file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
    
def load_object(path: str):
    try:
        with open(path,"rb") as file:
          return  pickle.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

    

