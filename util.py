import json
import pickle
import numpy as np

__locations = None
__data_columns = None
__model = None


def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(240)
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1
    return round(__model.predict([x])[0])


def get_location_names():
    return __locations


def load_saved_artifacts():
    print("loading...starts")
    global __data_columns
    global __locations
    global __model

    with open(r"C:\Users\HP\OneDrive\Desktop\mainfold\artifacts\columns.json") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]

    with open(r"C:\Users\HP\OneDrive\Desktop\mainfold\banglore_home_prices_model.pickle", 'rb') as f:
        __model = pickle.load(f)
    print("loading...done")


if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('Marathahalli', 1519, 6, 5))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2))
    print(get_estimated_price('Ejipura', 4000, 2, 2))
