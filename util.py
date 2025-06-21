import json
import pickle
import numpy as np

__locations = None
__data_columns = None
__model = None


def get_estimated_price(location, sqft, bhk, bath, balcony=1):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    x[3] = balcony  # Now properly includes balcony feature
    
    if loc_index >= 0:
        x[loc_index] = 1
    
    try:
        prediction = __model.predict([x])[0]
        return round(prediction, 2)
    except Exception as e:
        print(f"Prediction error: {e}")
        return 50.0  # Default fallback price


def get_location_names():
    return __locations


def load_saved_artifacts():
    print("loading...starts")
    global __data_columns
    global __locations
    global __model

    with open("columns.json") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]

    with open("banglore_home_prices_model.pickle", 'rb') as f:
        __model = pickle.load(f)
    print("loading...done")


if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('Marathahalli', 1519, 6, 5))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2))
    print(get_estimated_price('Ejipura', 4000, 2, 2))
