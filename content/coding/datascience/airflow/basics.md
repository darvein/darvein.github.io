# Airflow basics



## Introduction

Example of 	the DAG dashboard

![image-20210217224429399](image-20210217224429399.png)

## DAG Creation

A DAG (Directed acyclic graph) is a set of tasks connected between them, it has a start and an end.

Example: Create table -> Is API Available -> Extract data -> Store user -> process user

**Skeleton example:**

```
airflow.cfg airflow.db dags/ logs/ unitests.cfg webserver_config.py
```

Sample of a DAG user_processing.py

```python
from airflow.models import DAG
from datetime import datetime
from airflow.providers.sqlite.operators.sqlite import SqliteOperator

default_args = {
    'start_date': datetime(2020, 1, 1)
}

with DAG('user_processing', schedule_interval='@daily',
         default_args=default_args,
         catchup=False) as dag:
    
    create_table = SqliteOpreator(
        task_id='creating_table',
        sqlite_conn_id='db_sqlite',
        sql='''
        CREATE TABLE users (
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            country TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL PRIMARY KEY
        );
        '''
    )
```

Then start the airflow webserver: `airflow webserver` and also `airflow scheduler`

**Types of operators**

- Action operators: execute action
- Transfer operators: transfer data
- Sensors: wait for a condition to be met

**Notes**:

- Remember to use 1 operator and 1 task, it is not a N-to-N relationship, it must be 1:1



