from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.logger import logging
from src.exception import NetworkSecurityException
from src.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
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
        print(data_validation_artifact)
    except Exception as e :
        raise NetworkSecurityException(e,sys)