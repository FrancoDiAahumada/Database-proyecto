# Librerías
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
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
        print(f"Error al crear el engine de PostgreSQL: {e}")
        return None


def extract_table(table_name: str) -> pd.DataFrame:
    """
    Extrae todos los datos de una tabla específica y devuelve el resultado como DataFrame.
    """
    engine = get_postgres_engine()
    if engine is None:
        return pd.DataFrame()

    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql_query(query, engine)
    return df


def extract_query(query: str) -> pd.DataFrame:
    """
    Ejecuta un query SQL personalizado y devuelve el resultado como DataFrame.
    """
    engine = get_postgres_engine()
    if engine is None:
        return pd.DataFrame()

    df = pd.read_sql_query(query, engine)
    return df
