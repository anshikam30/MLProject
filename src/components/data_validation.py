import os
import sys
import numpy as np
import pandas as pd


from src.logger import logging
from src.exception import NetworkSecurityException
from src.utils import read_yaml_file
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.constant.training_pipeline import SCHEMA_FILE_PATH
##for data drift:
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self, data_validation_config : DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_validation(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        