from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'run_external_script_hourly',
    default_args=default_args,
    description='Run external script from log-pipeline every hour',
    schedule='@hourly',
    catchup=False,
)

script_path = '/opt/airflow/dags/logs_to_minio.py'

run_script = BashOperator(
    task_id='run_log_pipeline_script',
    bash_command=f'python {script_path}',
    dag=dag,
)
