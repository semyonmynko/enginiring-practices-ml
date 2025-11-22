import logging
import os
import pickle

import pandas as pd
from config.loader import load_config
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from warppers import task_safe

DATA_PATH = "/opt/airflow/dags/data/data.csv"
TMP_DIR = "/opt/airflow/dags/tmp"
MODEL_PATH = "/opt/airflow/dags/models/model.pkl"


class MLPipeline:
    def __init__(self):
        os.makedirs(TMP_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        self.logger = logging.getLogger(self.__class__.__name__)

        self.df = pd.read_csv(DATA_PATH, encoding="latin1")

    @task_safe
    def load_data(self, **context):
        context["ti"].xcom_push(key="dataset_shape", value=self.df.shape)

    @task_safe
    def preprocess(self, **context):
        df = self.df.dropna(subset=["Quantity", "UnitPrice", "CustomerID"])
        df = df[["Quantity", "UnitPrice", "CustomerID"]]

        X = df[["UnitPrice", "CustomerID"]]
        y = df["Quantity"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        X_train.to_csv(f"{TMP_DIR}/X_train.csv", index=False)
        X_test.to_csv(f"{TMP_DIR}/X_test.csv", index=False)
        y_train.to_csv(f"{TMP_DIR}/y_train.csv", index=False)
        y_test.to_csv(f"{TMP_DIR}/y_test.csv", index=False)

        self.logger.debug(f"Train size={len(X_train)}, Test size={len(X_test)}")

    @task_safe
    def train_model(self, **context):
        X_train = pd.read_csv(f"{TMP_DIR}/X_train.csv")
        y_train = pd.read_csv(f"{TMP_DIR}/y_train.csv")

        if X_train.empty or y_train.empty:
            raise ValueError("Training data is empty")

        cfg = load_config("random_forest", "dataset")

        model = RandomForestRegressor(
            n_estimators=cfg.model.n_estimators, random_state=cfg.dataset.random_state
        )
        model.fit(X_train, y_train.values.ravel())

        pickle.dump(model, open(MODEL_PATH, "wb"))

    @task_safe
    def validate_model(self, **context):
        X_test = pd.read_csv(f"{TMP_DIR}/X_test.csv")
        y_test = pd.read_csv(f"{TMP_DIR}/y_test.csv")

        if X_test.empty or y_test.empty:
            raise ValueError("Validation data is empty")

        model = pickle.load(open(MODEL_PATH, "rb"))
        preds = model.predict(X_test)
        mse = mean_squared_error(y_test, preds)

        self.logger.info(f"Model MSE: {mse:.4f}")
        context["ti"].xcom_push(key="mse", value=mse)


class ErrorTestTasks:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @task_safe
    def load_data_error_test(self, **context):
        raise ConnectionError("Database temporarily unavailable")

    @task_safe
    def data_type_error_test(self, **context):
        raise TypeError
