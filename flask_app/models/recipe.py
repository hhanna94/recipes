from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    database_name = "recipes_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data["date_made"]
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def new_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, NOW(), NOW(), %(user_id)s);"
        results = connectToMySQL(cls.database_name).query_db(query,data)
        return results

    @classmethod
    def get_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE recipes.id=%(id)s;"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.database_name).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append ( cls(recipe) )
        return recipes

    @classmethod
    def update_recipe(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_made=%(date_made)s, under_30=%(under_30)s, updated_at=NOW() WHERE id=%(id)s;"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id=%(id)s;"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results

    @classmethod
    def validate(cls, data):
        is_valid = True
        if len(data['name']) < 3:
            flash("Recipe Name must be at least 3 characters.", "recipes")
            is_valid = False
        if len(data['description']) < 3:
            flash("Recipe Description must be at least 3 characters.", "recipes")
            is_valid = False
        if len(data['instructions']) < 3:
            flash("Recipe Instructions must be at least 3 characters.", "recipes")
            is_valid = False
        if not data['date_made']:
            flash("You must fill out the date you made the recipe on.", "recipes")
            is_valid = False
        if 'under_30' not in data:
            flash("You must select if the recipe is under 30 minutes or not.", "recipes")
            is_valid = False
        return is_valid
