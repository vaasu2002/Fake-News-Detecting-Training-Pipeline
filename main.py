from fakenews.configuration.mongo_db_connection import MongoDBClient
from fakenews.exception import FakeNewsException
from fakenews.logger import logging
from fakenews.pipeline.training_pipeline import TrainPipeline

if __name__ == '__main__':
    train_pipeline = TrainPipeline()
    train_pipeline.run_pipeline()