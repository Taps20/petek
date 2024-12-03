from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connections, orders, order=None):
    cursor = connections.cursor()

    order_query = ("INSERT INTO orders "
                   "(customer_name, customer_email, customer_phone, datetime)"
                   "VALUES (%s, %s, %s, %s)")
    order_data = (order['customer_name'], order['grand_total'], datetime.now())

    order_id = cursor.lastrowid
    order_details_query = ("INSERT INTO order_details "
                           "(order_id, product_id, order_quantity)"
                           "VALUES (%s, %s, %s)")

    order_details_data = []
    for order_details_record in orders['order_details']:
        order_details_data.append([
            order_id,
            int(order_details_record['product_id']),
            float(order_details_record['product_quantity'])
        ])
    cursor.executemany(order_details_query, order_details_data)

    connection.commit()

    return order_id

def get_order_details(connections, order_id):
    cursor = connections.cursor()

    query = "SELECT * from petek.order_details where order_id = %s"

    query = "SELECT order_details.order_id, order_details.order_quantity, "\
            "products.product_name, products.product_ingredients FROM order_details LEFT JOIN products on " \
            "order_details.product_id = products.product_id where order_details.order_id = %s"

    data = (order_id, )

    cursor.execute(query, data)

    records = []
    for (order_id, order_quantity, order_ingredients, product_name) in cursor:
        records.append({
            'order_id': order_id,
            'order_quantity': order_quantity,
            'order_ingredients': order_ingredients,
            'product_name': product_name
        })

    cursor.close()

    return records

def get_all_orders(connections):
    cursor = connections.cursor()
    query = "SELECT * FROM petek.orders"
    cursor.execute(query)
    response = []
    for (order_id, customer_name, customer_phone, customer_email, dt) in cursor:
        response.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'datetime': dt,
        })

    cursor.close()

    # append order details in each order
    for record in response:
        record['order_details'] = get_order_details(connection, record['order_id'])

    return response

if __name__ == '__main__':
    connection = get_sql_connection()
    print(get_all_orders(connection))