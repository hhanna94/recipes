from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")

class User:
    database_name = "recipes_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def new_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s, NOW(), NOW());"
        results = connectToMySQL(cls.database_name).query_db(query,data)
        return results

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * from users WHERE email=%(email)s"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def validate_registration(cls, data):
        is_valid = True
        query = "SELECT * from users WHERE email=%(email)s;"
        results = connectToMySQL(cls.database_name).query_db(query,data)
        if len(data['fname']) < 2:
            flash("First Name must be at least 2 characters.", "registration")
            is_valid = False
        if len(data['lname']) < 2:
            flash("Last Name must be at least 2 characters.", "registration")
            is_valid = False
        if not PASSWORD_REGEX.match(data['password']):
            flash("Password must be at least 8 characters, and have at least one number.", "registration")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords do not match.", "registration")
            is_valid = False
        if not results:
            if not EMAIL_REGEX.match(data['email']):
                flash("Invalid email address!", "registration")
                is_valid = False
        else:
            flash("This email already exists!", "registration")
            is_valid = False
        return is_valid
