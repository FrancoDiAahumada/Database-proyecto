import os
from google.cloud import bigquery
import pandas as pd

PROJECT_ID = os.getenv("GCP_PROJECT")
DATASET = os.getenv("GCP_DATASET") 
TABLE = os.getenv("GCP_TABLE")

def load_to_bigquery(df):
    """Carga un DataFrame de pandas a BigQuery"""
    try:
        client = bigquery.Client(project=PROJECT_ID)
        table_id = f"{PROJECT_ID}.{DATASET}.{TABLE}"
        
        # Configuración del job - ESTO ES CLAVE
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE",  # Reemplaza la tabla
            autodetect=True,  # Detecta automáticamente el esquema
            source_format=bigquery.SourceFormat.PARQUET  # Usa formato Parquet (requiere PyArrow)
        )
        
        # Cargar usando PyArrow explícitamente
        job = client.load_table_from_dataframe(
            df, 
            table_id, 
            job_config=job_config
        )
        
        job.result()  # Espera a que termine
        
        print(f"✅ {df.shape[0]} filas cargadas en {table_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error cargando a BigQuery: {e}")
        return False
    
    
    