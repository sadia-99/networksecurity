from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.execption.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

import sys

if __name__=='__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")
        print(dataingestionartifact)

        # TODO: re-add data validation, transformation and model training
        # once components/data_validation.py, data_transformation.py and
        # model_trainer.py are written.
    except Exception as e:
        raise NetworkSecurityException(e,sys)
