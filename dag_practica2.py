from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

#Inicialización del grafo DAG de tareas para el flujo de trabajo
dag = DAG(
    'practica2',
    default_args=default_args,
    description='Grafo práctica 2',
    schedule_interval=timedelta(days=1),
)

CrearEntornoBBDD = BashOperator(
    task_id='crearEntornoBBDD',
    bash_command= 
    'cd /tmp && git clone https://github.com/mjls130598/Practica2-CC.git' +
    '&& cd /tmp/Practica2-CC && docker-compose build',
    dag=dag
)

DescargaDatosA = BashOperator(
task_id='descargaA',
bash_command='cd /tmp && wget https://github.com/manuparra/MaterialCC2020/blob/master/humidity.csv.zip',
dag=dag,
)

DescargaDatosB = BashOperator(
task_id='descargaB',
bash_command='cd /tmp && wget https://github.com/manuparra/MaterialCC2020/blob/master/temperature.csv.zip',
dag=dag,
)

UnZipFicheros = BashOperator(
task_id='UnZipFicheros',
bash_command='unzip /tmp/humidity.csv.zip && unzip /tmp/temperature.csv.zip',
dag=dag,
)


#Dependencias
CrearEntornoBBDD >> [DescargaDatosA, DescargaDatosB] >> UnZipFicheros