from airflow.dags.config.loader import load_config

cfg = load_config("random_forest", "dataset")

print(cfg.dataset.random_state)
