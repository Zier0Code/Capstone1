from pymongo import MongoClient

class model_DB:
    def __init__(self, db_name, collection_name):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
    
    def insert_document(self, document):
        self.collection.insert_one(document)
    
    def display_connection(self):
        print('Connected to the database name \n Connected to the collectio name ' )
    
    def find_admin(self, document):
        return self.collection.find_one(document)

admin = model_DB('orca_db','admins')
result = admin.collection.find_one({'admin_email': 'avila.253943@ortigas-cainta.sti.edu.ph'})

print(result)
