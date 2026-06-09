from datetime import datetime, timedelta

# Operators; we need this to operate!
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator, PythonVirtualenvOperator
# The DAG object; we'll need this to instantiate a DAG
from airflow.sdk import DAG

def run_external_script(script_path):
    # The script must be accessible on the Airflow worker's filesystem
    #script_path = "$AIRFLOW_HOME/dags/soccer_analytics/etls/extract_fixture_id.py"
    
    # Ocorre erro se usar $AIRFLOW_HOME porque o Python não resolve variáveis de ambiente
    print("Executando esse PATH: ", script_path)
    with open(script_path, "r") as file:
        script_code = file.read()
        
    # Execute the file's code within the virtual environment context
    exec(script_code, globals())

with DAG(
    "soccer_analytics",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5)
    },
    description="Workflow for extracting, transforming, and loading soccer analytics data",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:
    
    #execute_script = BashOperator(
    #    task_id="extract_fixture_id",
    #    # Use AIRFLOW_HOME or absolute paths to prevent "file not found" errors
    #    bash_command="""
    #    pip install -r $AIRFLOW_HOME/dags/soccer_analytics/requirements.txt && \
    #    python $AIRFLOW_HOME/dags/soccer_analytics/etls/extract_fixture_id.py
    #    """, 
    #)

    extract_fixture_id = PythonVirtualenvOperator(
        task_id="extract_fixture_id",
        python_callable=run_external_script,
        op_kwargs={"script_path": "/opt/airflow/dags/soccer_analytics/etls/extract_fixture_id.py"},
        requirements=['psycopg', 'requests'], #"$AIRFLOW_HOME/dags/soccer_analytics/requirements.txt",
        system_site_packages=False
    )

    extract_league_id = PythonVirtualenvOperator(
        task_id="extract_league_id",
        python_callable=run_external_script,
        op_kwargs={"script_path": "/opt/airflow/dags/soccer_analytics/etls/extract_league_id.py"},
        requirements=['psycopg', 'requests'], #"$AIRFLOW_HOME/dags/soccer_analytics/requirements.txt",
        system_site_packages=False
    )

    extract_fixture_stats = PythonVirtualenvOperator(
        task_id="extract_fixture_stats",
        python_callable=run_external_script,
        op_kwargs={"script_path": "/opt/airflow/dags/soccer_analytics/etls/extract_fixture_stats.py"},
        requirements=['psycopg', 'requests'], #"$AIRFLOW_HOME/dags/soccer_analytics/requirements.txt",
        system_site_packages=False
    )

[extract_fixture_id, extract_league_id] 
extract_fixture_id >> extract_fixture_stats