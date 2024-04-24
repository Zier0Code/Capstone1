from conn import model_DB

model = model_DB('orca_db','admin_super')

class Admin_S:
    def __init__(self):
        self.__admin = "Angelo"
        self.__password = "1234"
    
    def insert_admin(self):
        self.document = {
            "admin": self.admin,
            "password": self.password
        }
        model.insert_document(self.document)
    
    def check_admin(self):
        self.document = {
            "admin": "Angelo"
        }
        result = model.find_admin(self.document)
        print(result)
