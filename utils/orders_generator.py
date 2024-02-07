import requests
import random

REQUESTS_TO_MAKE = 50000
NEW_ORDERS_INTERVAL = 5
URL = "http://10.100.11.131:3000/orders"

FOOD_ITEMS = ['Broccoli', 'Stew', 'Chocolate Bar', 'Onion']
ANIMAL_ITEMS = ['Dog', 'Cat', 'Tucan', 'Horse']
DECORATION_ITEMS = ['Table', 'Plate']
ANIMAL_FOOD_ITEMS = ['Dog Food', 'Cat Food']
TECH_ITEMS = ['Computer Mouse', 'Keyboard', 'Chocolate Bar']
ITEMS = [FOOD_ITEMS, ANIMAL_ITEMS,
         DECORATION_ITEMS, ANIMAL_FOOD_ITEMS, TECH_ITEMS]
POSSIBALE_COMBINATIONS = [[0, 2], [4, 2], [1, 3], [0, 2], [1, 3], [0, 4]]

request_skeleton = {
    "user": 0,
    "items": [],
    "address": "House seven in left",
    "orderDate": "2024-02-1"
}


def send_requests():
    request_index = 0

    while request_index < REQUESTS_TO_MAKE:
        if (request_index % NEW_ORDERS_INTERVAL == 0):
            request_skeleton["user"] = request_index // NEW_ORDERS_INTERVAL
            five_random_orders = generate_five_random_orders()

        request_skeleton["items"] = five_random_orders[request_index %
                                                       NEW_ORDERS_INTERVAL]
        x = requests.post(URL, json=request_skeleton)

        if (x.status_code != 201):
            print(x.text)

        print(request_index)
        request_index += 1


def generate_five_random_orders():
    order_index = 0
    orders = []
    main_order_type_index = random.randint(0, len(ITEMS))

    while order_index < NEW_ORDERS_INTERVAL:
        order_type = random.choice([random.choice(POSSIBALE_COMBINATIONS),
                                    POSSIBALE_COMBINATIONS[main_order_type_index], 
                                    POSSIBALE_COMBINATIONS[main_order_type_index], 
                                    POSSIBALE_COMBINATIONS[main_order_type_index], 
                                    POSSIBALE_COMBINATIONS[main_order_type_index]])
        orders.append(get_random_order(order_type[0], order_type[1]))
        order_index += 1

    return orders


def get_random_order(i, j):
    order_items = []
    items_in_order = random.choice([1, 2, 3, 4, 5])

    while len(order_items) < items_in_order:
        random_item = random.choice(
            [random.choice(ITEMS[i]), random.choice(ITEMS[j])])

        if random_item not in map(lambda order: order["itemName"], order_items):
            order_items.append({
                "itemName": random_item,
                "itemQuantity": 1
            })

    return order_items


send_requests()
