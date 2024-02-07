import tensorflow as tf
import requests
import json
import pandas as pd
import numpy as np
import csv
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

TRAIN_TEST_RATIO = 0.8

items_dict = {
    'Broccoli': 0,
    'Horse': 1,
    'Stew': 2,
    'Tucan': 3,
    'Keyboard': 4,
    'Computer Mouse': 5,
    'Plate': 6,
    'Table': 7,
    'Chocolate Bar': 8,
    'Onion': 9,
    'Dog Food': 10,
    'Dog': 11,
    'Cat': 12,
    'Cat Food': 13
}

CATEGORIES = len(items_dict)
print(CATEGORIES)

orders = []

with open('shop.orders.short.csv') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        if row[0] != "user":
            orders.append(row)

orders = list(map(lambda order:
                  {
                      "user": order[0],
                      "items": sorted(list(map(lambda item: items_dict[item], order[1: (order.index('') if '' in order else -1)])))
                  },
                  orders))

print(orders[0])


def get_xy(orders):
    X_TO_Y_RATIO = 5

    x, y = np.array([]), np.array([])
    index = 0

    while index < len(orders):
        temp_order = np.array(orders[index]["items"])

        if (index + 1) % X_TO_Y_RATIO != 0:
            x = np.append(x, replace_categorial_input(temp_order))
        else:
            y = np.append(y, replace_categorial_input(temp_order))

        index += 1

    return x.reshape(44680, 4 * CATEGORIES), y.reshape(44680, CATEGORIES)


def replace_categorial_input(input):
    output = [0] * CATEGORIES

    for index in input:
        output[index] = 1

    return output


x, y = get_xy(orders)
print(x.shape)

train_length = int(len(x) * TRAIN_TEST_RATIO)
train_x, train_y = x[:train_length], y[:train_length]
test_x, test_y = x[train_length:], y[train_length:]

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(CATEGORIES, activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss=tf.keras.losses.Poisson(),
    metrics=tf.keras.metrics.TopKCategoricalAccuracy(
        k=4, name='top_k_categorical_accuracy', dtype=None)
)

model.build(input_shape=(None, 56))


model.fit(train_x, train_y, epochs=10)
model.evaluate(test_x,  test_y, verbose=2)

model.save('../model/recommendation_model.h5')


def softmax(x):
    return np.array(np.exp(x)/sum(np.exp(x)))


predictions = model.predict(test_x[2].reshape(1, 4 * CATEGORIES))
print(predictions)

for prediction in predictions:
    softmax_predict = softmax(prediction)
    print(np.where(softmax_predict == np.amax(softmax_predict))[0])
