import pandas as pd

def calculate_sales_by_customer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma un DataFrame de órdenes + detalles para calcular ventas totales por cliente.
    Espera columnas: customer_id, company_name, unit_price, quantity
    """
    df["total_line"] = df["unit_price"] * df["quantity"]
    result = (
        df.groupby(["customer_id", "company_name"], as_index=False)
          .agg(total_sales=("total_line", "sum"))
          .sort_values("total_sales", ascending=False)
    )
    return result
