from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd

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
    'cd /tmp && git clone https://github.com/mjls130598/Practica2-CC.git',
    dag=dag
)

DescargaDatosA = BashOperator(
    task_id='descargaA',
    bash_command='cd /tmp/Practica2-CC && ' +
    'wget https://github.com/manuparra/MaterialCC2020/raw/master/humidity.csv.zip',
    dag=dag,
)

DescargaDatosB = BashOperator(
    task_id='descargaB',
    bash_command='cd /tmp/Practica2-CC '
        '&& wget https://github.com/manuparra/MaterialCC2020/raw/master/temperature.csv.zip',
    dag=dag,
)

UnZipFicheros = BashOperator(
    task_id='unZipFicheros',
    bash_command='unzip /tmp/Practica2-CC/humidity.csv.zip -d /tmp/Practica2-CC && '
        'unzip /tmp/Practica2-CC/temperature.csv.zip -d /tmp/Practica2-CC',
    dag=dag,
)

# Función para fusionar columnas
def fusionarDatos():
    # Abrir los ficheros de los datos
    temperatura = pd.read_csv("/tmp/Practica2-CC/temperature.csv")
    humedad = pd.read_csv("/tmp/Practica2-CC/humidity.csv")

    # Para cada tabla, obtener las columnas fecha y San Francisco
    temperatura_select = temperatura[['datetime', 'San Francisco']]
    humedad_select = humedad[['datetime', 'San Francisco']]

    # Para cada tabla, cambiar la columna San Francisco por el nombre de la tabla
    temperatura_renombre = temperatura_select.rename(columns={'San Francisco': 'temperature'})
    humedad_renombre = humedad_select.rename(columns={'San Francisco': 'humidity'})

    # Unir ambas tablas por la columna fecha
    union = pd.merge(temperatura_renombre, humedad_renombre, on="datetime")
    union.to_csv("/tmp/Practica2-CC/datos.csv")

FusionarDatos = PythonOperator(
    task_id='fusionarDatos',
    provide_context=True,
    python_callable=fusionarDatos,
    dag=dag
)

AlmacenarBBDD = BashOperator(
    task_id='almacenarBBDD',
    bash_command='cd /tmp/Practica2-CC && docker-compose run web python enviarBBDD.py',
    dag=dag,
)

#Dependencias
CrearEntornoBBDD >> [DescargaDatosA, DescargaDatosB] >> UnZipFicheros >> FusionarDatos >> AlmacenarBBDD