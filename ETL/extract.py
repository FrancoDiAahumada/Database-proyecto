# Librerías
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

def get_postgres_engine():
    """Devuelve un engine de SQLAlchemy para PostgreSQL."""
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
            f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )
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
