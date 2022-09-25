from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Customer:

    db = "yard_wizard_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.address_line1 = data['address_line1']
        self.address_line2 = data['address_line2']
        self.city = data['city']
        self.state = data['state']
        self.zip = data['zip']
        self.lawn_sqft = data['lawn_sqft']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO customers (first_name, last_name, address_line1, address_line2, city, state, zip, lawn_sqft, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(address_line1)s, %(address_line2)s, %(city)s, %(state)s, %(zip)s, %(lawn_sqft)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM customers WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if not result:
            return False
        else:
            return cls(result[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM customers;"
        results = connectToMySQL(cls.db).query_db(query)
        if not results:
            return []
        customers = []
        for customer in results:
            customers.append(cls(customer))
        return customers

    @classmethod
    def update(cls, data):
        query = "UPDATE customers SET first_name = %(first_name)s, last_name = %(last_name)s, address_line1 = %(address_line1)s, address_line2 = %(address_line2)s, city = %(city)s, state = %(state)s, zip = %(zip)s, lawn_sqft = %(lawn_sqft)s, updated_at = NOW() WHERE id = %(id)s;"

    @staticmethod
    def validate_customer(customer):
        is_valid = True
        if len(customer['first_name']) < 2:
            is_valid = False
            flash("First name is too short, must be a least 2 characters")
        if len(customer['last_name']) < 2:
            is_valid = False
            flash("Last name is too short, must be a least 2 characters")
        if len(customer['address_line1']) < 1:
            is_valid = False
            flash("Please enter an address")
        if len(customer['city']) < 1:
            is_valid = False
            flash("Please enter a city")
        if len(customer['state']) < 1:
            is_valid = False
            flash("Please enter a state")
        if len(customer['zip']) < 5:
            is_valid = False
            flash("Please enter a valid zip code")
        
        return is_valid