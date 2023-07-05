from flask_app.config.mysqlconnection import ConnectToMySQL
from flask import flash
from flask_app.models import user
from datetime import datetime


class Guest:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.food_selection = data['food_selection']
        self.favorite_memory = data['favorite_memory']
        self.user_id = data['user_id']


    @classmethod 
    def create_guest(cls, data):
        query = "INSERT into GUESTS (name, food_selection, favorite_memory, user_id) VALUES (%(name)s, %(food_selection)s, %(favorite_memory)s,  %(user_id)s)"
        import json
        print(json.dumps(data, indent=4))
        return ConnectToMySQL('guests_schema').query_db(query, data)
    

    @classmethod
    def get_guests(cls):
        query = "SELECT * from GUESTS JOIN users on guests.user_id = users.id"
        results = ConnectToMySQL('guests_schema').query_db(query, {})
        GUESTS = []
        for row in results:
            user_data = {
                "id": row['user_id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password_hash": row['password_hash'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
            u = user.User(user_data)
            guest = Guest(row)
            guest.added_by = u
            Guest.append(guest)
        return guest
    
    
    @classmethod
    def get_guest_by_id(cls, data):
        query = "SELECT * FROM GUESTS JOIN users on guests.user_id = users.id WHERE guests.id = %(id)s"
        result = ConnectToMySQL('guests_schema').query_db(query, data)
        if not result: 
            return False 
        
        result = result[0]
        guest = cls(result)
        form_data = {
            'id': result['user_id'],
            'first_name': result['first_name'],
            'last_name': result['last_name'],
            'email': result['email'],
            'password_hash': result['password_hash'],
            'created_at': result['created_at'],
            'updated_at': result['updated_at'],
        }
        guest.added_by = user.User(form_data)
        return guest
    
    @classmethod
    def get_guests_by_user(cls, user):
        query = "SELECT * FROM guests WHERE user_id = %(id)s"
        results = ConnectToMySQL('guests_schema').query_db(query, {"id": user.id})
        if not results or len(results) == 0: 
            return []
        
        guests = []
        for row in results:
            guest = cls(row)
            guest.added_by = user
            guests.append(guest)
        return guests

    
    
    @classmethod
    def edit_guest(cls, data):
        data['under30'] = 1 if data['under30'] == 'yes' else 0
        query = """
        UPDATE guests SET name=%(name)s, food_selection=%(food_selection)s, 
        favorite_memory=%(favorite_memory)s, updated_at=NOW(), WHERE id = %(id)s;
        """
        return ConnectToMySQL ('guests_schema').query_db(query, data)
    
    @classmethod
    def delete_guest(cls, data):
        query = "DELETE FROM GUESTS WHERE id = %(id)s"
        return ConnectToMySQL ('guests_schema').query_db(query, data)
    
    @staticmethod
    def validate_guest(form_data):
        import json
        print(json.dumps(form_data, indent=4))
        is_valid = True
        if len(form_data['name']) < 3:
            flash("name must be 3 characters or more")
            is_valid = False
        if len(form_data ['food_selection']) < 3:
            flash ("food_selection must be 3 characters or more")
            is_valid = False
        if len(form_data['favorite_memory']) < 3:
            flash ("favorite_memory must be 3 characters or more")
            is_valid = False
        return is_valid
    


        


    


    


        
