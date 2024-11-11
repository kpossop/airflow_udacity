
markdown
Copiar código
# 📢 **Importante**

Lo contenido en este repositorio de GitHub es una réplica del proyecto que se desarrolló en el espacio de trabajo proporcionado por Udacity para el modulo de AUTOMATE DATA PIPELINES . Todos los servicios de Airflow fueron levantados, desarrollados y ejecutados en dicho entorno de trabajo.

# Proyecto: Pipelines de Datos Automatizados con Airflow

## Descripción General
Este proyecto implementa un pipeline de datos automatizado para una empresa de streaming de música, Sparkify, utilizando Apache Airflow para orquestar y automatizar procesos de ETL que extraen, transforman y cargan datos en un almacén de datos en Amazon Redshift. El pipeline se basa en operadores personalizados de Airflow y tareas configuradas para garantizar la correcta ingesta y verificación de calidad de los datos.

## Estructura del Proyecto
El proyecto está organizado en las siguientes carpetas y archivos:

```plaintext
├── README.md                   # Documentación del proyecto
├── airflow                     # Configuraciones de Airflow
├── assets                      # Archivos de soporte visual
│   ├── Ejecucion exitosa.png   # Captura de pantalla de una ejecución exitosa del DAG
│   └── duracion ejecucion.png  # Captura de pantalla de la duración de la ejecución del DAG
├── dags                        # Carpeta principal de los DAGs de Airflow
│   ├── cd0031-automate-data-pipelines # Proyecto principal de Airflow
│   │   ├── docker-compose.yaml        # Archivo de configuración de Docker Compose para Airflow
│   │   └── project
│   │       └── starter
│   │           ├── final_project.py   # DAG principal del proyecto
│   │           └── final_project_operators  # Operadores personalizados
│   │               ├── data_quality.py      # Operador para comprobaciones de calidad de datos
│   │               ├── load_dimension.py    # Operador para cargar tablas de dimensiones
│   │               ├── load_fact.py         # Operador para cargar tablas de hechos
│   │               └── stage_redshift.py    # Operador para cargar datos de S3 a Redshift
│   └── udacity
│       └── common
│           └── final_project_sql_statements.py # Declaraciones SQL auxiliares para transformaciones
└── plugins                                  # Carpeta de plugins de Airflow
    └── final_project_operators
        ├── data_quality.py
        ├── load_dimension.py
        ├── load_fact.py
        └── stage_redshift.py
```
