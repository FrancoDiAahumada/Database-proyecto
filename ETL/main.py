from extract import extract_data
from transform import calculate_sales_by_customer
from load import load_to_bigquery



def main():
    # Query corregida con unión a clientes para obtener company_name 
    query = """
    SELECT c.customer_id,
           c.company_name,
           od.unit_price,
           od.quantity
    FROM orders o
    JOIN order_details od ON o.order_id = od.order_id
    JOIN customers c ON o.customer_id = c.customer_id;
    """

    # --- EXTRACT ---
    df_orders = extract_data(query=query)
    
    if df_orders.empty:
        print("⚠️ No se extrajeron datos de la base de datos. Abortando ETL.")
        return

    print(f"[INFO] Se extrajeron {df_orders.shape[0]} filas.")

    # --- TRANSFORM ---
    df_summary = calculate_sales_by_customer(df_orders)
    print(f"[INFO] Transformación completada. {df_summary.shape[0]} filas de resumen generadas.")

    # --- LOAD ---
    try:
        load_to_bigquery(df_summary)
        print("[INFO] ETL completado con éxito.")
    except Exception as e:
        print(f"[ERROR] Falló la carga a BigQuery: {e}")

# --- ENTRYPOINT para Cloud Function ---
def etl_entrypoint(request):
    """
    Handler que usa Google Cloud Functions.
    No recibe parámetros, solo ejecuta el pipeline.
    """
    main()
    return "ETL ejecutado con éxito."

if __name__ == "__main__":
    main()
