import os
from flask import Flask, render_template, redirect, flash, session, request, jsonify, url_for, json
from models import db, connect_db, User, Recipe
from forms import UserForm, LoginForm, RecipeForm, MealPlanForm, IngredientForm
from flask_bcrypt import  bcrypt

from dotenv import load_dotenv
import requests

app = Flask(__name__)

load_dotenv('key.env')


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///mealmate')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'super'

connect_db(app)


@app.route('/')
def home():
    user = session.get('user_id')
    return render_template('base.html', user=user)


@app.route('/search-recipes', methods=['GET'])
def search_recipes():
   
    if 'user_id' in session:
        search_query = request.args.get('q')

        if not search_query:
            return jsonify({'error': 'Search query parameter "q" is missing'}), 400

        edamam_api_url = 'https://api.edamam.com/api/recipes/v2'

        edamam_app_id = os.environ.get('APP_ID')
        edamam_app_key = os.environ.get('KEY')

        params = {
            'type': 'any',
            'q': search_query,
            'app_id': edamam_app_id,
            'app_key': edamam_app_key
        }
        

        try:
            user = session.get('user_id')
            response = requests.get(edamam_api_url, params=params)
            response.raise_for_status()

            data = response.json()
        
            
            return render_template('recipes.html', recipes=data.get('hits', []), user=user)

        except requests.RequestException as e:
            return jsonify({'error': str(e)}), 500
    else:
        flash('Please login to access this page.', 'danger')
        return redirect('/login')
    



@app.route('/login', methods=['GET'])
def login():
    form = LoginForm()
    user = session.get('user_id')
    return render_template('/users/login.html', form=form, user=user)

@app.route('/login', methods=['POST'])
def login_user():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        if user:
            session['user_id'] = user.user_id
            return redirect('/user_home')
        else:
            form.username.errors = ['Invalid username or password.']
            return render_template('/users/login.html', form=form, user=user)
    else:
        return redirect('/login')


@app.route('/user_home')
def user_home():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        recipe = Recipe.query.filter_by(user_id=user_id).all()
        if user:
            return render_template('/users/user_home.html', user=user, recipe=recipe)
    flash('Please login to access this page.', 'danger')
    return redirect('/login')

@app.route('/register', methods=['GET'])
def register():
    form = UserForm()
    return render_template('/users/register.html', form=form)

@app.route('/register', methods=['POST'])
def register_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
        
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()
        
        return redirect('/login')
    else:
        session['user'] = None
        return render_template('/users/register.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/login')


@app.route('/get_recipes/<string:mealType>')

def get_recipes(mealType):
    # Define the endpoint and parameters for the Edamam API request
    edamam_api_url = 'https://api.edamam.com/api/recipes/v2'
    
    edamam_app_id = os.environ.get('APP_ID')
    edamam_app_key = os.environ.get('KEY')
    params = {
        'type': 'any',
        'q': mealType,
        'app_id': edamam_app_id,
        'app_key': edamam_app_key
    }

    try:
        response = requests.get(edamam_api_url, params=params)
        response.raise_for_status()

        data = response.json()

        return render_template('recipes.html', recipes=data.get('hits', []))

    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_recipes_<string:dishType>')

def get_recipes_(dishType):
    # Define the endpoint and parameters for the Edamam API request
    edamam_api_url = 'https://api.edamam.com/api/recipes/v2'
    
    edamam_app_id = os.environ.get('APP_ID')
    edamam_app_key = os.environ.get('KEY')
    params = {
        'type': 'any',
        'q': dishType,
        'app_id': edamam_app_id,
        'app_key': edamam_app_key
    }

    # Make a GET request to the Edamam API
    try:
        response = requests.get(edamam_api_url, params=params)
        response.raise_for_status()

        data = response.json()

        return render_template('recipes.html', recipes=data.get('hits', []))

    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
    
# Meal plan route

@app.route('/meal_plan', methods=['GET'])
def meal_plan():
    user = session.get('user_id')
    if 'user_id' in session:
        form = MealPlanForm()
        return render_template('meal_planner.html', form=form, user=user)
    
    else:
        flash('Please login to access this page.', 'danger')
        return redirect('/login')
 

@app.route('/meal_plan', methods=['POST'])
def meal_plan_post():
    user = session.get('user_id')
    if 'user_id' not in session:
        form = MealPlanForm()
        if form.validate_on_submit():
            timeFrame = form.timeFrame.data
            targetCalories = form.targetCalories.data
            diet = form.diet.data
            exclude = form.exclude.data
            return redirect('/get_meal_plan?timeFrame={}&targetCalories={}&diet={}&exclude={}'.format(timeFrame, targetCalories, diet, exclude))
        else:
            return render_template('meal_planner.html', form=form, user=user)
    else:
        flash('Please login to access this page.', 'danger')
        return redirect('/login')

@app.route('/get_meal_plan', methods=['GET'])
def get_meal_plan():
    user = session.get('user_id')
    timeFrame = request.args.get('timeFrame')
    targetCalories = request.args.get('targetCalories')
    diet = request.args.get('diet')
    exclude = request.args.get('exclude')
    
    api_Key = os.environ.get('SPOONACULAR_API_KEY')
    spoonacular_api_url = 'https://api.spoonacular.com/mealplanner/generate'

    params = {
        'timeFrame': timeFrame,
        'targetCalories': targetCalories,
        'diet': diet,
        'exclude': exclude
    }
    
    headers = {
        'x-api-key': api_Key,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(spoonacular_api_url, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()

        meals = data.get('meals', [])
        
        for meal in meals:
            meal['image'] = f"https://spoonacular.com/recipeImages/{meal['id']}-556x370.{meal['imageType']}"

        nutrients = data.get('nutrients', {})  

        return render_template('user_meal_plans.html', meals=meals, nutrients=nutrients, user=user)

    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
    
# user recipes route


@app.route('/create_recipe', methods=['GET', 'POST'])
def create_recipe():
    
    user = session.get('user_id')
    form = RecipeForm()

    if request.method == 'POST':
        if request.method == 'POST':
            if 'user_id' in session:
                user_id = session['user_id']
                
                # Processing ingredients
                ingredients = []
                for ingredient_form in form.ingredients:
                    title = ingredient_form.title.data
                    quantity = ingredient_form.quantity.data
                    measure = ingredient_form.measure.data
                    ingredients.append({'title': title, 'quantity': quantity, 'measure': measure})
                
                # Creating recipe object
                recipe = Recipe(
                    title=form.title.data,
                    image_url=form.image_url.data,
                    source_name=form.source_name.data,
                    source_url=form.source_url.data,
                    servings=form.servings.data,
                    ingredients=ingredients,
                    calories=form.calories.data,
                    total_fat=form.total_fat.data,
                    cholesterol=form.cholesterol.data,
                    sodium=form.sodium.data,
                    total_carbohydrates=form.total_carbohydrates.data,
                    protein=form.protein.data,
                    user_id=user_id
                )

                db.session.add(recipe)
                db.session.commit()

                flash('Recipe created successfully.', 'success')
                return redirect(url_for('user_home'))
            else:
                flash('Please log in to create a recipe.', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Please correct the errors in the form.', 'danger')

    return render_template('/users/user_recipe_form.html', form=form, user=user)




@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    user = session.get('user_id')
    recipe = Recipe.query.get_or_404(recipe_id)
    
    return render_template('view_recipe.html', recipe=recipe, user=user)

@app.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    user = session.get('user_id')
    recipe = Recipe.query.get_or_404(recipe_id)
    form = RecipeForm(obj=recipe)
    if request.method == 'POST':
        recipe.title = form.title.data
        recipe.image_url = form.image_url.data
        recipe.source_name = form.source_name.data
        recipe.source_url = form.source_url.data
        recipe.servings = form.servings.data
        recipe.calories = form.calories.data
        recipe.total_fat = form.total_fat.data
        recipe.cholesterol = form.cholesterol.data
        recipe.sodium = form.sodium.data
        recipe.total_carbohydrates = form.total_carbohydrates.data
        recipe.protein = form.protein.data
        
        

        ingredients = []
        for ingredient_form in form.ingredients:
            title = ingredient_form.title.data
            quantity = ingredient_form.quantity.data
            measure = ingredient_form.measure.data
            ingredients.append({'title': title, 'quantity': quantity, 'measure': measure})
            
        recipe.ingredients = ingredients

        db.session.commit()
        flash('Recipe updated successfully.', 'success')
        return redirect(url_for('view_recipe', recipe_id=recipe.id), user=user)
    
    else:
        return render_template('edit_recipe.html', form=form, recipe=recipe)



@app.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    user = session.get('user_id')
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted successfully.', 'success')
    return redirect(url_for('user_home', user=user))

if __name__ == '__main__':
    app.run(debug=True)

