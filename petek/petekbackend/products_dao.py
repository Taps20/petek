from sql_connection import get_sql_connection

def get_all_products(connections):
    cursor = connections.cursor()
    query = "SELECT * FROM petek.products"
    cursor.execute(query)
    response = []
    for (product_id, product_name, product_ingredients) in cursor:
        response.append({
            'product_id': product_id,
            'product_name': product_name,
            'product_ingredients': product_ingredients

        })
    return response
def insert_new_product(connections, product):
    cursor = connection.cursor()
    query = ("INSERT INTO products "
             "(product_name, product_ingredients)"
             "VALUES (%s, %s)")
    data = (product['product_name'], product['product_ingredients'])
    cursor.execute(query, data)
    connection.commit()

    return cursor.lastrowid

def delete_product(connections, product_id):
    cursor = connections.cursor()
    query = ("DELETE FROM products WHERE product_id =" + str(product_id))
    cursor.execute(query)
    connection.commit()

    return cursor.lastrowid

if __name__ == '__main__':
    connection = get_sql_connection()
    print(insert_new_product(connection, {
        'product_name': 'banana_bread',
        'product_ingredients': 'butter, redvelvet'
    }))


