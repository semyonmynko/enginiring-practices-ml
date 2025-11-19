import time

import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import (AdaBoostClassifier, ExtraTreesClassifier,
                              GradientBoostingClassifier,
                              RandomForestClassifier)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.svm import SVC

iris = load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

models = [
    ("RandomForest", RandomForestClassifier(n_estimators=100)),
    ("LogisticRegression", LogisticRegression(max_iter=200)),
    ("SVM", SVC()),
    ("GradientBoosting", GradientBoostingClassifier()),
    ("AdaBoost", AdaBoostClassifier()),
    ("ExtraTrees", ExtraTreesClassifier(n_estimators=100)),
]

for name, model in models:
    with mlflow.start_run():
        start_time = time.time()

        cv_scores = cross_val_score(model, X_train, y_train, cv=10, scoring="accuracy")
        accuracy = cv_scores.mean()

        mlflow.log_param("model", name)
        mlflow.log_param("n_estimators", model.get_params().get("n_estimators", None))

        mlflow.log_metric("accuracy", accuracy)

        training_time = time.time() - start_time
        mlflow.log_metric("training_time", training_time)

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        precision = precision_score(y_test, y_pred, average="weighted", zero_division=1)
        recall = recall_score(y_test, y_pred, average="weighted", zero_division=1)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=1)

        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

        mlflow.sklearn.log_model(model, f"{name}_model")

        print(
            f"Logged {name} with accuracy: {accuracy}, precision: {precision}, recall: {recall}, f1: {f1}, training_time: {training_time}s"
        )
