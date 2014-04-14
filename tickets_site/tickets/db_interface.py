from django.db import connection, transaction
from datetime import datetime


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

@transaction.atomic
def insert_customer(sql, cursor, **kwargs):
    cursor.execute("INSERT INTO customer (name, birthday, gender, phone_number) VALUES (%s, %s, %s, %s)", sql)
    cursor.execute("SELECT id FROM customer\
                    WHERE name LIKE %s\
                    ORDER BY id DESC\
                    LIMIT 1",\
                    [kwargs['name']])
    return cursor.fetchone()[0]

@transaction.atomic
def insert_ticket_order(sql, cursor, **kwargs):
    cursor.execute("INSERT INTO ticket_order (buy_date, customer_id, edition_id) VALUES (%s, %s, %s)", sql)
    cursor.execute("SELECT id FROM ticket_order\
                    WHERE customer_id = %s\
                    ORDER BY id DESC\
                    LIMIT 1", [sql[1]])
    return cursor.fetchone()[0]

def get_sum_price(cursor, pieces):
    cursor.execute("SELECT price, category FROM category_price c JOIN date_price d ON d.id = date_price_id WHERE edition_id = 1")
    d = dictfetchall(cursor)
    sum_price = 0
    for item in d:
        sum_price += item["price"] * pieces[item["category"]]
    return sum_price

def filter_categories(**kwargs):
    pieces = kwargs
    del pieces['name']
    del pieces['gender']
    del pieces['birthday']
    del pieces['phone']
    del pieces['event']
    return pieces

def buy_ticket(**kwargs):
    cursor = connection.cursor()

    sql = [kwargs['name'],
                kwargs['birthday'],
                kwargs['gender'],
                kwargs['phone']]
    customer_id = insert_customer(sql, cursor, **kwargs)
    sql = [datetime.now(),
                customer_id,
                kwargs['event']]
    order_id = insert_ticket_order(sql, cursor, **kwargs)

    pieces = filter_categories(**kwargs)
    price = get_sum_price(cursor, pieces)
    for category, piece in pieces.items():
        if piece:
            cursor.execute("INSERT INTO ticket (category, price, pieces, order_id) VALUES (%s, %s, %s, %s)", [category, price, piece, order_id])
    return tickets_response(cursor)

def tickets_response(cursor):
    # response assembling

    cursor.execute("SELECT c.id, c.name, date_part('year', age(c.birthday))::int AS age,\
                    e.label AS event_name, t.category, t.pieces, t.price, o.buy_date\
                    FROM customer c\
                    JOIN ticket_order o ON c.id = o.customer_id\
                    JOIN ticket t ON o.id = t.order_id\
                    JOIN event_edition e ON e.id = o.edition_id")

    d = dictfetchall(cursor)
    return dict_make(d, "pieces")
    
def dict_make(d, atr):
    a = {}
    for e in d:
        id = e["id"]
        if id not in a:
            a[id] = e
        a[id][e["category"]] = e[atr]
        if "category" in a[id]:
            del a[id]["category"]
        if atr in a[id]:
            del a[id][atr]

    arr = []
    for e in a:
        arr.append(a[e])

    return arr

def prices_response(cursor):
    # response assembling

    cursor.execute("SELECT d.id, e.label AS event_name, d.valid_from start_date, d.valid_to end_date, c.category, c.price\
                    FROM event_edition e\
                    JOIN date_price d ON e.id = d.edition_id\
                    JOIN category_price c ON d.id = c.date_price_id")

    d = dictfetchall(cursor)
    return dict_make(d, "price")

def get_prices():
    cursor = connection.cursor()
    prices = prices_response(cursor)
    return prices

def get_all_events():
    cursor = connection.cursor()
    cursor.execute("SELECT id, label AS name FROM event_edition")
    d = dictfetchall(cursor)
    return d

def get_all_date_events():
    cursor = connection.cursor()
    cursor.execute("SELECT d.id, label AS name, d.valid_from start_date, d.valid_to end_date FROM event_edition e\
                    JOIN date_price d ON e.id = d.edition_id")
    d = dictfetchall(cursor)
    print(d)
    return d

def filter_prices(**kwargs):
    prices = kwargs
    del prices['event']
    return prices

def update_prices(**kwargs):
    cursor = connection.cursor()
    prices = filter_prices(**kwargs)
    date_price_id = kwargs['event']
    for category, price in prices.items():
        if price:
            cursor.execute("UPDATE category_price SET price = %s WHERE category = %s AND date_price_id = %s", [price, category, date_price_id])
    return get_prices()

def delete_event(**kwargs):
    cursor = connection.cursor()
    event_id = kwargs['event']
    cursor.execute("DELETE FROM event_edition WHERE id = %s", [event_id])
    return get_all_events()
