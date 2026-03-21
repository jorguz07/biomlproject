import os
import sys

import numpy as np
import pandas as pd
import dill

from sklearn.metrics import r2_score

from src.exception import CustomException

def save_object(file_path, obj):
    ''' Saves given python object to given file_path '''
    try:
        dir_path = os.path.dirname( file_path )
        os.makedirs( dir_path, exist_ok=True )
        with open( file_path, 'wb' ) as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models( X_train, y_train, X_test, y_test, models ):
    try:
        report = {}
        for name, model in models.items(): #for each model
            model.fit(X_train, y_train) #train

            y_train_pred = model.predict(X_train) #predict on train
            y_test_pred = model.predict(X_test) #predict on test

            train_model_score = r2_score( y_train, y_train_pred ) #performance train
            test_model_score = r2_score( y_test, y_test_pred ) #performance test

            report[name] = {
                "train_score": train_model_score,
                "test_score": test_model_score
            }
        return report
    
    except Exception as e:
        raise CustomException(e, sys)
            