from fakenews.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
from fakenews.entity.artifact_entity import DataIngestionArtifact
from fakenews.exception import FakeNewsException
import sys,os
from fakenews.logger import logging
from fakenews.components.data_ingestion import DataIngestion
# from fakenews.components.data_validation import DataValidation



class TrainPipeline:
    def __init__(self):

        self.training_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
    
    def start_data_ingestion(self)->DataIngestionArtifact:

        try:
            
            logging.info("Starting Data Ingestion")

            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)

            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()

            logging.info(f"Data Ingestion completed. The artifact location:- {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise FakeNewsException(e,sys)
    
    def run_pipeline(self):
        try:
            logging.info(f"Starting re-training pipeline")
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()

        except Exception as e:
            raise FakeNewsException(e,sys)  