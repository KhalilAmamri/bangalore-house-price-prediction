import json
import pickle
import warnings
import os

warnings.filterwarnings('ignore')

__locations = None
__data_columns = None
__model = None

def get_location_names():
    return __locations

def get_estimated_price(location, sqft, bath, bhk):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = [0] * len(__data_columns)
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)



def load_saved_artifacts():
    print("Loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model

    # Use absolute path from current file location
    current_dir = os.path.dirname(os.path.abspath(__file__))  # /server
    models_dir = os.path.join(current_dir, '..', 'models')    # Go up to /models
    
    columns_path = os.path.join(models_dir, 'columns.json')
    model_path = os.path.join(models_dir, 'house_price_model.pkl')
    
    print(f"Looking for files at: {columns_path}")
    
    with open(columns_path, "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]

    with open(model_path, "rb") as f:
        __model = pickle.load(f)
    print("✓ Loading saved artifacts...done")


if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('Indira Nagar', 1000, 2, 2))

