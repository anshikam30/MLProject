from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.logger import logging
from src.exception import NetworkSecurityException
from src.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTranformationConfig, ModelTrainerConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtfiact
import sys 

if __name__ =="__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config= DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("initiate data ingestion.")
        data_ingestion_artifact: DataIngestionArtifact= data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed.")
        
        logging.info("Data Validation Initialised.")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_validation_config,data_ingestion_artifact)
        data_validation_artifact:DataValidationArtifact = data_validation.initiate_data_validation() 
        logging.info("Data Validation completed.")
        
        
        logging.info("Data Transformation Initialised.")
        data_transformation_config = DataTranformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config,data_validation_artifact)
        data_transformation_artifact : DataTransformationArtifact = data_transformation.initialise_data_transformation() 
        logging.info("Data Transformation completed.")
        
        logging.info("Model Trainer  Initialised.")
        model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        model_trainer= ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact : ModelTrainerArtfiact = model_trainer.initiate_model_trainer() 
        logging.info(model_trainer_artifact)
        logging.info("Model Trainer completed.")
        
    except Exception as e :
        raise NetworkSecurityException(e,sys)