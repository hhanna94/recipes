from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    if not session:
        return redirect("/")
    recipes = Recipe.get_recipes()
    user = {
        "user_id": session["user_id"],
        "user_name": session["name"]
    }
    return render_template("dashboard.html", recipes=recipes, user=user)

@app.route('/recipes/<int:id>')
def display_recipe(id):
    if not session:
        return redirect("/")
    id = {"id": id}
    recipe = Recipe.get_recipe(id)
    user_name = session["name"]
    return render_template("recipe_page.html", recipe=recipe, user_name=user_name)

@app.route('/recipes/new')
def new_recipe():
    if not session:
        return redirect("/")
    return render_template("new_recipe.html")

@app.route('/create', methods=["POST"])
def create():
    print(request.form)
    if not session:
        return redirect("/")
    if not Recipe.validate(request.form):
        return redirect('/recipes/new')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_made": request.form["date_made"],
        "under_30": request.form["under_30"],
        "user_id": session["user_id"]
    }
    Recipe.new_recipe(data)
    return redirect('/dashboard')

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if not session:
        return redirect("/")
    id = {"id": id}
    recipe = Recipe.get_recipe(id)
    return render_template("edit_recipe.html", recipe=recipe)

@app.route('/edit', methods=["POST"])
def edit():
    if not session:
        return redirect("/")
    recipe_user_id = int(request.form['user_id'])
    user_id = int(session['user_id'])
    if recipe_user_id != user_id:
        flash("You can't edit a recipe that doesn't belong to you.", "edit/delete")
        return redirect('/dashboard')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_made": request.form["date_made"],
        "under_30": request.form["under_30"],
        "id": request.form["recipe_id"]
    }
    if not Recipe.validate(request.form):
        return redirect('/recipes/edit/' + data['id'])
    Recipe.update_recipe(data)
    return redirect('/recipes/' + data['id'])

@app.route('/recipes/delete/<int:id>')
def delete(id):
    if not session:
        return redirect("/")
    data = {"id": id}
    Recipe.delete(data)
    return redirect('/dashboard')
