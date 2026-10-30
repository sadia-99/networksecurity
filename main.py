import mlflow
from mlflow.entities import SpanType

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import ModelTrainerConfig
 

import sys

mlflow.set_tracking_uri("https://dagshub.com/sadianaitkaoudjt/networksecurity.mlflow")
mlflow.set_experiment("my-experiment")


@mlflow.trace(name="training_pipeline", span_type=SpanType.CHAIN)
def run_pipeline():
    trainingpipelineconfig=TrainingPipelineConfig()
    dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
    data_ingestion=DataIngestion(dataingestionconfig)
    logging.info("Initiate the data ingestion")
    dataingestionartifact=mlflow.trace(name="data_ingestion", span_type=SpanType.CHAIN)(data_ingestion.initiate_data_ingestion)()
    logging.info("Data Initiation Completed")
    print(dataingestionartifact)
    data_validation_config=DataValidationConfig(trainingpipelineconfig)
    data_validation=DataValidation(dataingestionartifact,data_validation_config)
    logging.info("Initiate the data Validation")
    data_validation_artifact=mlflow.trace(name="data_validation", span_type=SpanType.CHAIN)(data_validation.initiate_data_validation)()
    logging.info("data Validation Completed")
    print(data_validation_artifact)
    data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
    logging.info("data Transformation started")
    data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
    data_transformation_artifact=mlflow.trace(name="data_transformation", span_type=SpanType.CHAIN)(data_transformation.initiate_data_transformation)()
    print(data_transformation_artifact)
    logging.info("data Transformation completed")

    logging.info("Model Training sstared")
    model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
    model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
    model_trainer_artifact=mlflow.trace(name="model_trainer", span_type=SpanType.CHAIN)(model_trainer.initiate_model_trainer)()

    logging.info("Model Training artifact created")
    return model_trainer_artifact


if __name__=='__main__':
    try:
        run_pipeline()
    except Exception as e:
           raise NetworkSecurityException(e,sys)
