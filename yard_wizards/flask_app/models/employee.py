from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Employee:
    
    db = "yard_wizard_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.applicator_id = data['applicator_id']
        self.email = data['email']
        self.password = data['password']
        self.dob = data['dob']
        self.date_hired = data['date_hired']
        self.date_terminated = data['date_terminated']
        self.admin = data['admin']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

    @classmethod
    def save(cls, data):
        query = "INSERT INTO employees (first_name, last_name, applicator_id, email, password, dob, date_hired, admin, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(applicator_id)s, %(email)s, %(password)s, %(dob)s, NOW(), 0, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM employees WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if not result:
            return False
        else:
            return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM employees WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if not result:
            return False
        else:
            return cls(result[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE employees SET first_name = %(first_name)s, last_name = %(last_name)s, dob = %(dob)s, email = %(email)s, applicator_id = %(applicator_id)s, date_hired = %(date_hired)s, date_terminated = %(date_terminated)s, updated_at = NOW();"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_employee(employee):
        is_valid = True
        if len(employee['first_name']) < 2:
            is_valid = False
            flash("First Name is too short, must be at least 2 characters")
        if len(employee['last_name']) < 2:
            is_valid = False
            flash("Last Name is too short, must be at least 2 characters")
        if len(employee['applicator_id']) < 10:
            is_valid = False
            flash("Please enter a valid applicator id")
        if not EMAIL_REGEX.match(employee['email']):
            is_valid = False
            flash('bad email')
        if len(employee['password']) < 8:
            is_valid = False
            flash("Password is too short, must be at least 8 characters")
        if employee['password'] != employee['confirm']:
            is_valid = False
            flash('passwords must match')

        return is_valid

