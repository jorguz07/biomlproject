import os
import sys
from dataclasses import dataclass

from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from catboost import CatBoostRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object, evaluate_models


@dataclass
class ModelTrainerConfig:
    best_model_storing_path = os.path.join('artifacts', 'model.pkl')


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array, train_df, test_df):
        """
        Trains multiple models and evaluates them using Weighted Pearson Correlation (WPC).
        Saves the best model and returns its WPC score.
        """

        try:
            # split arrays
            X_train, y_train = train_array[:, :-1], train_array[:, -1]
            X_test, y_test = test_array[:, :-1], test_array[:, -1]

            logging.info('Splitting training and test data completed')

            # models
            models = {
                "Linear Regression": LinearRegression(),
                "Lasso": Lasso(),
                "Ridge": Ridge(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest Regressor": RandomForestRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False, allow_writing_files=False),
                "AdaBoost Regressor": AdaBoostRegressor()
            }

            # hyperparameters
            params = {
                "Decision Tree": {'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson']},
                "Random Forest Regressor": {'n_estimators': [8, 16, 32, 64, 128, 256]},
                "Gradient Boosting": {
                    'learning_rate': [.1, .01, .05, .001],
                    'subsample': [0.6, 0.7, 0.8, 0.9],
                    'n_estimators': [8, 16, 32, 64, 128]
                },
                "Linear Regression": {},
                "Lasso": {'alpha': [0.01, 0.1, 1.0, 10.0]},
                "Ridge": {'alpha': [0.01, 0.1, 1.0, 10.0]},
                "K-Neighbors Regressor": {'n_neighbors': [3, 5, 7]},
                "XGBRegressor": {'learning_rate': [.1, .01], 'n_estimators': [50, 100]},
                "CatBoosting Regressor": {'depth': [6, 8], 'learning_rate': [0.01, 0.05], 'iterations': [30, 50]},
                "AdaBoost Regressor": {'learning_rate': [.1, .01], 'n_estimators': [50, 100]}
            }

            # evaluate
            model_report, best_models = evaluate_models(
                X_train_arr=X_train,
                y_train=y_train,
                X_test_arr=X_test,
                y_test=y_test,
                models=models,
                param=params,
                X_train_df=train_df,
                X_test_df=test_df
            )

            # best model selection
            best_model_name = max(model_report, key=model_report.get)
            best_model_score = model_report[best_model_name]
            best_model = best_models[best_model_name]

            if best_model_score is None or best_model_score < 0.01:
                raise CustomException("No valid best model found")

            logging.info(f"Best model: {best_model_name} with WPC: {best_model_score}")

            # save
            save_object(
                file_path=self.model_trainer_config.best_model_storing_path,
                obj=best_model
            )

            return best_model_score

        except Exception as e:
            raise CustomException(e, sys)