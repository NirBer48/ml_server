from flask import Flask
from flask import request
from flask_cors import CORS
from tensorflow.keras.models import load_model
import numpy as np
import json

app = Flask(__name__)
CORS(app)

model = load_model('./model/recommendation_model.h5')

ORDERS = 4

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


@app.route('/get-recommended-items', methods=['POST'])
def getRecommendedItems():
    data = json.loads(request.data)
    input = np.array([])
    index = 0

    while index < ORDERS:
        print(index - (len(data) * (index // len(data))))
        input = np.append(input, replace_categorial_input(
            data[index - (len(data) * (index // len(data)))]))

        index += 1

    return get_predictions(input)


def replace_categorial_input(items):
    output = [0] * len(items_dict)

    for item in items:
        output[items_dict[item]] = 1

    return output


def get_predictions(input):
    probability_arr = model.predict(input.reshape(1, len(input)))

    return list(map(lambda tuple: tuple[1],
                    sorted(zip(probability_arr[0], list(items_dict.keys())), reverse=True)[:5]))
