from extract import extract_query
from transform import calculate_sales_by_customer

def main():
    query = """
        SELECT c.customer_id,
            c.company_name,
            od.unit_price, 
            od.quantity
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN order_details od ON o.order_id = od.order_id;
    """
    df = extract_query(query)
    result_df = calculate_sales_by_customer(df)
    print(result_df.head(5))

if __name__ == "__main__":
    main()
