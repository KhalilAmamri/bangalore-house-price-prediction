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
    models_dir = os.path.normpath(os.path.join(current_dir, '..', 'models'))  # Normalize the path
    
    columns_path = os.path.join(models_dir, 'columns.json')
    model_path = os.path.join(models_dir, 'house_price_model.pkl')
    
    print(f"Looking for columns.json at: {columns_path}")
    print(f"File exists: {os.path.exists(columns_path)}")
    print(f"Looking for model at: {model_path}")
    print(f"File exists: {os.path.exists(model_path)}")
    
    try:
        with open(columns_path, "r") as f:
            __data_columns = json.load(f)['data_columns']
            __locations = __data_columns[3:]
            print(f"✓ Loaded {len(__locations)} locations")
    except Exception as e:
        print(f"✗ Error loading columns: {e}")
        raise

    try:
        with open(model_path, "rb") as f:
            __model = pickle.load(f)
            print("✓ Model loaded successfully")
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        raise
    
    print("✓ Loading saved artifacts...done")


if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('Indira Nagar', 1000, 2, 2))

