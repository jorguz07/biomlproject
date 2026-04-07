import os
import sys

import numpy as np
import pandas as pd
import dill

from scipy.stats import pearsonr
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)


def weighted_pearson(df, combo_col='Combination', actual_col='Actual', pred_col='Predicted'):
    weighted_sum = 0
    weight_total = 0

    for combo, group in df.groupby(combo_col):
        n_i = len(group)

        if n_i <= 1:
            continue

        # skip constant arrays (prevents NaN explosions)
        if group[actual_col].nunique() <= 1 or group[pred_col].nunique() <= 1:
            continue

        rho_i, _ = pearsonr(group[actual_col], group[pred_col])
        weight = np.sqrt(n_i - 1)

        weighted_sum += weight * rho_i
        weight_total += weight

    if weight_total == 0:
        return np.nan

    return weighted_sum / weight_total


def evaluate_models(
    X_train_arr, y_train,
    X_test_arr, y_test,
    models, param,
    X_train_df, X_test_df
):
    """
    Evaluates models using ONLY Weighted Pearson Correlation (WPC)
    """

    try:
        report = {}
        best_models = {}

        # precompute combinations
        combo_train = X_train_df['Compound A'].astype(str) + "+" + X_train_df['Compound B'].astype(str)
        combo_test = X_test_df['Compound A'].astype(str) + "+" + X_test_df['Compound B'].astype(str)

        for name, model in models.items():

            para = param.get(name, {})

            if para:
                gs = GridSearchCV(model, para, cv=3, error_score=np.nan)
                gs.fit(X_train_arr, y_train)
                best_model = gs.best_estimator_
            else:
                model.fit(X_train_arr, y_train)
                best_model = model

            # predictions
            y_train_pred = best_model.predict(X_train_arr)
            y_test_pred = best_model.predict(X_test_arr)

            # evaluation dfs
            df_train_eval = pd.DataFrame({
                'Combination': combo_train,
                'Actual': y_train,
                'Predicted': y_train_pred
            })

            df_test_eval = pd.DataFrame({
                'Combination': combo_test,
                'Actual': y_test,
                'Predicted': y_test_pred
            })

            train_score = weighted_pearson(df_train_eval)
            test_score = weighted_pearson(df_test_eval)

            report[name] = test_score
            best_models[name] = best_model

    except Exception as e:
        raise CustomException(e, sys)

    return report, best_models