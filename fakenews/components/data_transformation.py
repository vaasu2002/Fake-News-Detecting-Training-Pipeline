# Importing Dependencies
import sys

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from fakenews.constant.training_pipeline import TARGET_COLUMN
from fakenews.entity.artifact_entity import (
    DataTransformationArtifact,
    DataIngestionArtifact,
)

from sklearn.feature_extraction.text import CountVectorizer
from fakenews.entity.config_entity import DataTransformationConfig
from fakenews.exception import FakeNewsException
from fakenews.logger import logging
from fakenews.ml.model.estimator import TargetValueMapping
from fakenews.ml.model.cleaning import nltk_preprocess
from fakenews.utils.main_utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self,data_ingestion_config:DataIngestionArtifact,
                data_transformation_config:DataTransformationConfig):
        """
            Creating the data transformation component of pipeline
            according to the flowchart.
            Args:
                self (object): Output reference of data ingestion artifact stage
                self (object): Configuration for data transformation
        """
        try:
            self.data_validation_artifact = data_ingestion_config
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise FakeNewsException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise FakeNewsException(e, sys)

    
    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        """ Creating preprocessing object for data transformation 
        Raises:
            FakeNewsException
        Returns:
            Pipeline: Preprocessing Pipeline object
        """
        try:
            count_vectorizer = CountVectorizer()
            # Creating preprocessing pipeline
            preprocessor_pipeline = Pipeline(
                steps=[
                    ("count_vectorizer", count_vectorizer)
                ]
            )
            
            return preprocessor_pipeline

        except Exception as e:
            raise FakeNewsException(e, sys) from e


    def initiate_data_transformation(self,) -> DataTransformationArtifact:
        try:
            # train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path) 
            # test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            train_df = DataTransformation.read_data(self.data_validation_artifact.training_file_path) 
            test_df = DataTransformation.read_data(self.data_validation_artifact.testing_file_path)



            preprocessor_pipeline = self.get_data_transformer_object()


            # Spliting Training DataFrame
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1) # Input Feature
            target_feature_train_df = train_df[TARGET_COLUMN] # Target Feature
            target_feature_train_df = target_feature_train_df.replace(TargetValueMapping().to_dict())


            # Spliting Testing DataFrame
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1) # Input Feature
            target_feature_test_df = test_df[TARGET_COLUMN] # Target Feature
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping().to_dict())


            logging.info(f"Performing NLTK pre-processing on training data")
            input_feature_train_df["title"] = input_feature_train_df.title.apply(nltk_preprocess)

            logging.info(f"Performing NLTK pre-processing on testing data")
            input_feature_test_df["title"] = input_feature_test_df.title.apply(nltk_preprocess)


            input_feature_train_array = np.array(input_feature_train_df['title'])
            input_feature_test_array = np.array(input_feature_test_df['title'])


            preprocessor_obj = preprocessor_pipeline.fit(input_feature_train_array)

            
            

            #  preprocessor_obj = preprocessor_pipeline.fit(input_feature_train_df)
            


            logging.info(f"Performing PreProcessing(CountVectorizer) on training data")

            transformed_input_train_feature = preprocessor_obj.transform(input_feature_train_array)

            # transformed_input_train_feature = preprocessor_obj.transform(input_feature_train_df)

            logging.info(f"Performing PreProcessing(CountVectorizer) on testing data")
            transformed_input_test_feature =preprocessor_obj.transform(input_feature_test_array)


            target_feature_train_array = np.array(target_feature_train_df)
            target_feature_test_array = np.array(target_feature_test_df)


            transformed_input_train_feature = transformed_input_train_feature.toarray()
            transformed_input_test_feature = transformed_input_test_feature.toarray()


            target_feature_train_array = target_feature_train_array.reshape(-1,1)

            target_feature_test_array = target_feature_test_array.reshape(-1,1)
            
            logging.info(transformed_input_train_feature.shape)
            logging.info(target_feature_train_array.shape)

            # Concatenating features 

            train_arr = np.concatenate((transformed_input_train_feature,target_feature_train_array), axis=1)
            test_arr = np.concatenate((transformed_input_test_feature,target_feature_test_array), axis=1)


            # train_arr = np.c_[np.array(df['title']), np.array(target_feature_train_final)]
            # test_arr = np.c_[ np.array(df['title']), np.array(target_feature_test_df)]
            

            #  Saving numpy array
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, 
                                  array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path
                                 ,array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path
                        ,preprocessor_obj)
            
            
            # Preparing artifacts
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            logging.info(f"Data transformation artifact: {data_transformation_artifact}")

            return data_transformation_artifact

        except Exception as e:
            raise FakeNewsException(e, sys) from e 