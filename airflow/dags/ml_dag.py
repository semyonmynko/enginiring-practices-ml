from datetime import datetime, timedelta

from airflow.operators.python import PythonOperator
from alerting import on_failure_callback
from pipelines import ErrorTestTasks, MLPipeline

from airflow import DAG

default_args = {
    "owner": "ml_team",
    "on_failure_callback": on_failure_callback,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=10),
}


with DAG(
    dag_id="ml_pipeline_dag",
    default_args=default_args,
    description="ML pipeline implemented as a class with each method as a task",
    schedule="0 9 * * *",
    start_date=datetime(2025, 11, 20),
    catchup=True,
    tags=["ml", "pipeline"],
) as dag:
    pipeline = MLPipeline()
    error_pipeline = ErrorTestTasks()

    load_data_error_test_task = PythonOperator(
        task_id="load_data_error_test",
        python_callable=error_pipeline.load_data_error_test,
        provide_context=True,
    )

    data_type_error_test_task = PythonOperator(
        task_id="data_type_error_test",
        python_callable=error_pipeline.data_type_error_test,
        provide_context=True,
    )

    t1 = PythonOperator(
        task_id="load_data", python_callable=pipeline.load_data, provide_context=True
    )

    t2 = PythonOperator(
        task_id="preprocess_data",
        python_callable=pipeline.preprocess,
        provide_context=True,
    )

    t3 = PythonOperator(
        task_id="train_model",
        python_callable=pipeline.train_model,
        provide_context=True,
    )

    t4 = PythonOperator(
        task_id="validate_model",
        python_callable=pipeline.validate_model,
        provide_context=True,
    )

    t1 >> t2 >> t3 >> t4
