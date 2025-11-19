from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from exp_utils_and_decs import (log_experiment, log_metrics,
                                log_params_and_model)

iris = load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)


@log_experiment
def train_random_forest(X_train, y_train, X_test, y_test):
    params = {"model": "random_forest_model", "n_estimators": 100, "max_depth": 10}

    model = RandomForestClassifier(
        n_estimators=params["n_estimators"], max_depth=params["max_depth"]
    )
    model.fit(X_train, y_train)

    log_params_and_model(model, params["model"], params)
    log_metrics(model, X_test, y_test)

    return model


train_random_forest(X_train, y_train, X_test, y_test)
