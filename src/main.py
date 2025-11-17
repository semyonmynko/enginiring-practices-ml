import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

iris = pd.read_csv("src/data/iris_dataset.csv")

X = iris[["Id", "SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]]
y = iris[["Species"]]

model = RandomForestClassifier()
model.fit(X, y)

model_name = "random_forest_model_v4"

mlflow.set_tracking_uri("sqlite:///mlflow.db")

with mlflow.start_run():
    mlflow.log_param("model_type", "RandomForestClassifier")
    mlflow.log_param("dataset", "Iris")
    mlflow.log_metric("accuracy", 0.95)
    mlflow.set_tag("experiment_name", "iris_classification")
    mlflow.set_tag("version", "1.0")

    mlflow.sklearn.log_model(model, "random_forest_model", input_example=X[:5])

    run_id = mlflow.active_run().info.run_id

mlflow.register_model(f"runs:/{run_id}/random_forest_model", model_name)
