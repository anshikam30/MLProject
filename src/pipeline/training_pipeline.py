from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

from src.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTranformationConfig, ModelTrainerConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtfiact

import sys 
from src.logger import logging
from src.exception import NetworkSecurityException


class Training_Pipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        
    
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config= DataIngestionConfig(self.training_pipeline_config)
            data_ingestion = DataIngestion(self.data_ingestion_config)
            logging.info("initiate data ingestion.")
            self.data_ingestion_artifact: DataIngestionArtifact= data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed.")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_validation(self):
        try:
            logging.info("Data Validation Initialised.")
            self.data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(self.data_validation_config,self.data_ingestion_artifact)
            self.data_validation_artifact:DataValidationArtifact = data_validation.initiate_data_validation() 
            logging.info("Data Validation completed.")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_transformation(self):
        try:
            logging.info("Data Transformation Initialised.")
            self.data_transformation_config = DataTranformationConfig(self.training_pipeline_config)
            data_transformation = DataTransformation(self.data_transformation_config,self.data_validation_artifact)
            self.data_transformation_artifact : DataTransformationArtifact = data_transformation.initialise_data_transformation() 
            logging.info("Data Transformation completed.")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_trainer(self):
        try:
            logging.info("Model Trainer  Initialised.")
            self.model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
            model_trainer= ModelTrainer(model_trainer_config=self.model_trainer_config, data_transformation_artifact=self.data_transformation_artifact)
            self.model_trainer_artifact : ModelTrainerArtfiact = model_trainer.initiate_model_trainer() 
            logging.info(self.model_trainer_artifact)
            logging.info("Model Trainer completed.")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    def run_pipeline(self):
        try:
            self.start_data_ingestion()
            self.start_data_validation()
            self.start_data_transformation()
            self.start_model_trainer()
            return self.model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)