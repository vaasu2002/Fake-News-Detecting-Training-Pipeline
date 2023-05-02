import os

# Pipeline Name and Root Directory Constant

SAVED_MODEL_DIR = os.path.join("saved_models")
TARGET_COLUMN = "Target"
PIPELINE_NAME: str = "fakenews"
ARTIFACT_DIR: str = "artifact"

# common file name

FILE_NAME: str = "fakenews.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"
MODEL_FILE_NAME = "model.pkl"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")


# Data Ingestion related constant start with DATA_INGESTION VAR NAME

DATA_INGESTION_COLLECTION_NAME: str = "dataset"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2


# Data Transformation ralated constant start with DATA_TRANSFORMATION VAR NAME

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"