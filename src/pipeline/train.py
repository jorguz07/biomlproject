from src.components.data_ingestion import DataIngestion
from src.components.data_transform import DataTransformation
from src.components.model_trainer import ModelTrainer

import pandas as pd

def run_training_pipeline():
    # --- Data Ingestion ---
    obj = DataIngestion()
    train_data_path, test_data_path = obj.initiate_data_ingestion()

    # --- Read original unprocessed DataFrames for WPC ---
    train_df_orig = pd.read_csv(train_data_path)
    test_df_orig = pd.read_csv(test_data_path)

    # --- Data Transformation ---
    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(
        train_data_path, test_data_path
    )

    # --- Model Training ---
    modeltrainer = ModelTrainer()
    best_model_wpc = modeltrainer.initiate_model_trainer(
        train_array=train_arr,
        test_array=test_arr,
        train_df=train_df_orig,
        test_df=test_df_orig
    )

    print(f"Best model Weighted Pearson Correlation on test set: {best_model_wpc:.4f}")


if __name__ == "__main__":
    run_training_pipeline()