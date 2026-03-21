#this module defines the data transform component
# - splits training and testing arrays into dep and ind vars
# - trains and tests on a catalogue of models
# - saves best model object
# - returns r2 of best model object

import os
import sys
from dataclasses import dataclass

from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from catboost import CatBoostRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object
from src.utils import evaluate_models

#class to store vars, to be used in model trainer
@dataclass
class ModelTrainerConfig:
    best_model_storing_path = os.path.join( 'artifacts','model.pkl' )

#class for data training
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig() #creates instance of ModelTrainerConfig class

    def initiate_model_trainer(self, train_array, test_array):
        ''' Given preprocessed train and test data as arrays, applies a selection of models and evaluates them with R2.
         Saves best model object and resturs its r2 '''
        try:
            #dep and ind vars from train and test dfs
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1], #take everything but the last col
                train_array[:,-1], #take last col
                test_array[:,:-1],
                test_array[:,-1]

            )
            logging.info( 'Splitting trianing and test data completed' )
        
            #models dicc
            models = {
                "Linear Regression": LinearRegression(),
                "Lasso": Lasso(),
                "Ridge": Ridge(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest Regressor": RandomForestRegressor(),
                "XGBRegressor": XGBRegressor(), 
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor()
            }

            #evaluate models and report
            model_report:dict = evaluate_models( X_train = X_train, y_train = y_train, X_test = X_test, y_test = y_test,
                                               models=models )
            
            #best model
            best_model_score = max( model_report.values() ) #best model score
            best_model_name = max( model_report, key=model_report.get ) #best model name
            best_model = models[best_model_name]

            if best_model_score < 0.01: #if no best model cancel
                raise CustomException( "No best model found" )
            logging.info( f'Best found model on both trianing and testing dataset' )

            #save best model object, we want to use it later
            save_object(
                file_path = self.model_trainer_config.best_model_storing_path,
                obj=best_model
            )

            predicted = best_model.predict( X_test )
            r2_square = r2_score( y_test, predicted )
            return r2_square

        except Exception as e:
            raise CustomException(e, sys)
