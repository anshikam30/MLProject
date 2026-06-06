from src.components.data_ingestion import DataIngestion
from src.logger import logging
from src.exception import NetworkSecurityException
from src.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
import sys 

if __name__ =="__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config= DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("initiate data ingestion.")
        artifact = data_ingestion.initiate_data_ingestion()
        
        print(artifact)
    except Exception as e :
        raise NetworkSecurityException(e,sys)