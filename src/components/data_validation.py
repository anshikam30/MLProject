import os
import sys
import numpy as np
import pandas as pd


from src.logger import logging
from src.exception import NetworkSecurityException
from src.utils.main_utils.utils import read_yaml_file, write_yaml_file
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
    
    
    @staticmethod
    def read_data(file_path)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    def validate_num_of_columns(self, df:pd.DataFrame)->bool:
        try:
            num_of_cols = len(self.schema_config)
            logging.info(f"Required Columns: {num_of_cols} ")
            logging.info(f"DataFrame has {len(df.columns)} number of columns.")
            
            if len(df.columns) != num_of_cols : return False
            
            return True
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def detect_data_drift(self,base_df,current_df, threshold=0.05):
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1= base_df[column]
                d2= current_df[column]
                
                is_sample_distribution_same = ks_2samp(d1,d2)
                if threshold <= is_sample_distribution_same.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update(
                    {
                        column: { 
                            "p_value": float(is_sample_distribution_same.pvalue),
                            "drift_status": is_found
                            }
                    }
                )
            dir_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(dir_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(dir_file_path, content=report)
            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path , test_file_path = self.data_ingestion_artifact.trained_file_path, self.data_ingestion_artifact.test_file_path
            
            ##read data from test and train files.
            
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)
            
            train_val = self.validate_num_of_columns(train_df)
            test_val = self.validate_num_of_columns(test_df)
            if not train_val:
                error_msg = f"Train Data frame does not contain all columns. \n"
                print(error_msg)
            if not test_val:
                error_msg = f"Test Data frame does not contain all columns. \n"
                print(error_msg)
                
            status = self.detect_data_drift(train_df, test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            train_df.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True
            )
            test_df.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )
            
            data_validation_artifact = DataValidationArtifact(
                validation_status= status,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        