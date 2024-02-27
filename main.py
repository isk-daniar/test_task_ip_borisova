import psycopg2

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="task_shop_db",
    user="postgres",
    password="postgres"
)


def get_products_by_orders(order_numbers):
    # Формируем строку с номерами заказов для использования в SQL-запросе
    order_numbers_str = ','.join(str(order) for order in order_numbers)

    # SQL-запрос для получения товаров, сгруппированных по стеллажам, для заданных номеров заказов
    query = """
        SELECT s.name AS shelving_name, p.id AS product_id, ps.order_number AS order_number, ps.quantity AS quantity, 
            ps.add_shelving AS add_shelving, p.name AS product_name
        FROM ProductShelves ps
        INNER JOIN Shelving s ON ps.shelving_id  = s.id
        INNER JOIN Products p ON ps.product_id = p.id
        ORDER BY s.name
    """.format(order_numbers_str)

    # Выполнение SQL-запроса
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()

    # Группировка товаров по стеллажам
    products_by_shelves = {}
    for row in rows:
        shelving_name, product_id, order_number, quantity, add_shelving, product_name = row
        if shelving_name not in products_by_shelves:
            products_by_shelves[shelving_name] = []
        products_by_shelves[shelving_name].append((product_id, order_number, quantity, add_shelving, product_name,))

    # Вывод товаров по стеллажам
    print("=+=+=+=")
    print("Страница сборки заказов", order_numbers_str)
    print("")
    for shelf_name, products  in products_by_shelves.items():
        print("===Стеллаж", shelf_name)
        products.sort(key=lambda x: x[1])  # Сортировка по номеру заказа
        for product_id, order_number, quantity, add_shelving, product_name, in products:
            print(product_name, "(id={})".format(product_id))
            print(f"заказ {order_number}, {quantity} шт")
            if add_shelving:
                print("доп стеллаж:", add_shelving)
            print("")
    # Закрытие соединения с базой данных
    cur.close()
    conn.close()

if __name__ == "__main__":
    import sys

    # Получение номеров заказов из аргументов командной строки
    order_numbers = sys.argv[1].split(',')

    # Вызов функции для получения товаров по стеллажам для заданных номеров заказов
    get_products_by_orders(order_numbers)