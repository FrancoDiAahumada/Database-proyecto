# Librerías
import os
import pandas as pd
from sqlalchemy import create_engine

# NO usar dotenv en Cloud Functions
# load_dotenv() <- REMOVER ESTA LÍNEA

def get_postgres_engine():
    try:
        # Obtener variables con valores por defecto
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        db = os.getenv("POSTGRES_DB", "northwind")
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "")
        
        # Validar que port sea numérico
        if port == "None" or not port or not port.isdigit():
            port = "5432"
            
        print(f"[DEBUG] Conectando a {host}:{port}/{db} con usuario {user}")
            
        engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")
        return engine
    except Exception as e:
        print(f"[ERROR] al crear el engine de PostgreSQL: {e}")
        return None

def extract_data(table_name: str = None, query: str = None) -> pd.DataFrame:
    """
    Extrae datos desde PostgreSQL.
    Puedes pasar table_name para extraer toda la tabla o query SQL personalizada.
    """
    if table_name is None and query is None:
        raise ValueError("[ERROR] Debes pasar 'table_name' o 'query'")

    engine = get_postgres_engine()
    if engine is None:
        print("[ERROR] No se pudo crear el engine de PostgreSQL")
        return pd.DataFrame()

    # Construir query si solo se pasa table_name
    if table_name:
        query = f"SELECT * FROM {table_name};"

    try:
        df = pd.read_sql_query(query, engine)
        print(f"[INFO] Se extrajeron {df.shape[0]} filas")
        return df
    except Exception as e:
        print(f"[ERROR] al ejecutar la query: {e}")
        return pd.DataFrame()