#this module defines the data transform component
# - builds preprocessing and transformation piepline
# - transforms data
# - saves pipeline object

import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object

#class to store vars, to be used in data itransformation
@dataclass #to avoid __init__ (mostly only for data containers!)
class DataTransformationConfig:
    preprocessor_obj_file_path: str=os.path.join('artifacts', 'preprocessor.pkl')

#class for data transformation
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig() #creates instance of DataTransformationConfig class

    #build preprocessor
    def get_data_transformer_object(self, numerical_features, categorical_features):
        ''' Given lists of num and cat vars, builds preprocessing object '''
        try:
            #def num and cat pipelines
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')), #missing vals
                    ('scaler', StandardScaler()) #standarize
                ]
            )
            logging.info( 'Numerical vars standard scalling completed' )

            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
                ]
            )
            logging.info( 'Categorical vars encoding completed' )

            #preprocessor: applies diff transforms to diff cols
            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline', num_pipeline, numerical_features),
                    ('cat_pipeline', cat_pipeline, categorical_features),
                ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
    
    #applies preprocessor
    def initiate_data_transformation(self, train_path, test_path):
        ''' Given train and test data paths, applies preprocessing object '''
        try:
            #read data
            train_df = pd.read_csv( train_path )
            test_df = pd.read_csv( test_path )
            logging.info( 'Reading train and test data completed' )

            #dependent and independent vars
            target_var = 'Synergy score'
            
            target_train_df = train_df[target_var]
            target_test_df = test_df[target_var]

            input_train_df = train_df.drop(columns=[target_var])
            input_test_df = test_df.drop(columns=[target_var])

            logging.info( f"Train input shape: {input_train_df.shape}" )
            logging.info( f"Train target shape: {target_train_df.shape}" )

            #build preprocessing object
            numerical_features = input_train_df.select_dtypes(include=np.number).columns.tolist()
            categorical_features = input_train_df.select_dtypes(include="object").columns.tolist()

            logging.info(f"Numerical features: {numerical_features}")
            logging.info(f"Categorical features: {categorical_features}")

            preprocessing_obj = self.get_data_transformer_object(
            numerical_features,
            categorical_features
            )  
            logging.info( 'Processing object built' )

            #apply preprocessing object
            logging.info( 'Applying preprocessing object on training and testig dfs' )
            input_feature_train_arr = preprocessing_obj.fit_transform( input_train_df ) #fit on train
            input_feature_test_arr = preprocessing_obj.transform( input_test_df ) #apply on test

            logging.info(f"Transformed train shape: {input_feature_train_arr.shape}")

            train_arr = np.c_[ input_feature_train_arr, target_train_df.values.reshape(-1,1) ] #change to array
            test_arr = np.c_[ input_feature_test_arr, target_test_df.values.reshape(-1,1) ]

            #save fitted preprocessing object
            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            logging.info( 'Fit processing object saved' )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)
