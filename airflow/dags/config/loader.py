# config/loader.py

import yaml

from .base_config import DatasetConfig, FullConfig, ModelConfig


def load_yaml(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_config(model_name: str, dataset_name: str) -> FullConfig:
    model_cfg = load_yaml(f"/opt/airflow/dags/config/models/{model_name}.yaml")
    dataset_cfg = load_yaml(f"/opt/airflow/dags/config/datasets/{dataset_name}.yaml")

    return FullConfig(
        model=ModelConfig(**model_cfg), dataset=DatasetConfig(**dataset_cfg)
    )
