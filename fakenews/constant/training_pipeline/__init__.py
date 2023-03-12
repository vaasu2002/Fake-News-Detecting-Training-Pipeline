import os

# Pipeline Name and Root Directory Constant

SAVED_MODEL_DIR = os.path.join("saved_models")
TARGET_COLUMN = "Target"
PIPELINE_NAME: str = "fakenews"
ARTIFACT_DIR: str = "artifact"

# Data Ingestion related constant start with DATA_INGESTION VAR NAME

DATA_INGESTION_COLLECTION_NAME: str = "dataset"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2