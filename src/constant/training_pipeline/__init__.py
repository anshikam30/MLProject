import os 
import sys
import numpy as np
import pandas as pd

'''
Defining common constants variable for training pipeling
'''

TARGET_COLUMN: str  = "Result"
PIPELINE_NAME: str  = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phishingData.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
SCHEMA_FILE_PATH : str = os.path.join("data_Schema", "schema.yaml")
SAVED_MODEL_DIR :str = os.path.join("saved_models")
'''
Data Ingestion related constants
'''

DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "ANSHIKAAI"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2


'''
Data Validation related constants
'''

DATA_VALIDATION_DIR_NAME: str = 'data_validation'
DATA_VALIDATION_VALID_DIR : str = 'validated'
DATA_VALIDATION_INVALID_DIR : str = 'invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR : str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME : str = 'drift_report.yaml'

'''
Data Tranformation related constants
'''

DATA_TRANSFORMATION_DIR_NAME: str = 'data_transformation'
DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_NAME : str = 'preprocessing.pkl'
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict ={
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform"    
}



'''
Model Trainer related constants
'''

MODEL_TRAINER_DIR_NAME = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR_NAME = "trained_model"
MODEL_FILE_NAME = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE = 0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD = 0.05

TRAINING_BUCKET_NAME = "networksecurity"