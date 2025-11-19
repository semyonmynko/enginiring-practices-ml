import mlflow


def log_metrics(model, X, y):
    accuracy = model.score(X, y)
    mlflow.log_metric("accuracy", accuracy)


def log_params_and_model(model, model_name, params):
    for param, value in params.items():
        mlflow.log_param(param, value)
    mlflow.sklearn.log_model(model, model_name)


def log_experiment(func):
    def wrapper(*args, **kwargs):
        with mlflow.start_run():
            result = func(*args, **kwargs)

            mlflow.log_param("model_type", func.__name__)

            if hasattr(result, "score"):
                accuracy = result.score(args[2], args[3])
                mlflow.log_metric("accuracy", accuracy)
            return result

    return wrapper
