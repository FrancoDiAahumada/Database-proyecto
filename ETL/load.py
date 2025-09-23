import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT")
DATASET = os.getenv("GCP_DATASET")
TABLE = os.getenv("GCP_TABLE")

def load_to_bigquery(df):
    """Carga un DataFrame de pandas a BigQuery"""
    client = bigquery.Client(project=PROJECT_ID)

    table_id = f"{PROJECT_ID}.{DATASET}.{TABLE}"

    job = client.load_table_from_dataframe(df, table_id)
    job.result()  # Espera a que termine

    print(f"✅ {df.shape[0]} filas cargadas en {table_id}")
    return