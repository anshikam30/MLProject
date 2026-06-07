
import numpy as np
import pandas as pd
import os, sys

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline


from src.exception import NetworkSecurityException
from src.logger import logging
from src.utils import save_numpy_array , save_object
from src.entity.config_entity import DataTranformationConfig
from src.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from src.constant.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS


class DataTransformation:
    def __init__(self, data_transformation_config: DataTranformationConfig, data_validation_artifact:DataValidationArtifact):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def read_data(file_path) ->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def handle_missing_values_usingKNNImputer(self) -> Pipeline:
        try:
            knn = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor = Pipeline([("imputer", knn)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    
    def initialise_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Starting Data Tranformation.")
            
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            ##Removing target column:
            
            input_feature_train_df = train_df.drop(TARGET_COLUMN, axis=1)
            input_feature_test_df = test_df.drop(TARGET_COLUMN, axis=1)
            
            target_train_df = train_df[TARGET_COLUMN].replace(-1, 0)
            target_test_df = test_df[TARGET_COLUMN].replace(-1, 0)
            
            ##KNN Imputer preprocessor
            
            preprocessor = self.handle_missing_values_usingKNNImputer()
            obj = preprocessor.fit(input_feature_train_df)
            obj_train = obj.transform(input_feature_train_df)
            obj_test = obj.transform(input_feature_test_df)
            
            train_arr = np.c_[obj_train, np.array(target_train_df)]
            test_arr = np.c_[obj_test, np.array(target_test_df)]
            
            preprocessor_file_path = self.data_transformation_config.preprocessing_pkl_file_path
            train_file_path = self.data_transformation_config.transformed_train_file_path
            test_file_path = self.data_transformation_config.transformed_test_file_path
            save_numpy_array(path=train_file_path, array=train_arr)
            save_numpy_array(path=test_file_path, array=test_arr)
            save_object(obj=preprocessor, path=preprocessor_file_path)
            
            data_transform_artifact = DataTransformationArtifact(
                transformed_object_file_path=preprocessor_file_path,
                transformed_test_npy_path=test_file_path,
                transformed_train_npy_path=train_file_path
            )
            
            return data_transform_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)