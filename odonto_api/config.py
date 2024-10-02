from pymongo import MongoClient

def get_db():
    try:
        client = MongoClient('localhost', 27017)
        db = client['Materiales_odontologia']
        collection = db['Productos']
        return collection
    except Exception as e:
        print(f"Error {e}")
