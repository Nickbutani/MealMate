from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField, FieldList, FormField
from wtforms.validators import InputRequired, Email, Length, NumberRange, DataRequired


class UserForm(FlaskForm):
    
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=1, max=255)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=1, max=255)])
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=255)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=1, max=255)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=1, max=255)])
    submit = SubmitField('Submit')
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=255)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=1, max=255)])
    submit = SubmitField('Submit')
    
class IngredientForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    quantity = FloatField('Quantity', validators=[DataRequired()])
    measure = StringField('Measure', validators=[DataRequired(), Length(max=50)])
    
class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=255)])
    image_url = StringField('Image URL', validators=[Length(max=255)])
    source_name = StringField('Source Name', validators=[Length(max=255)])
    source_url = StringField('Source URL', validators=[Length(max=255)])
    servings = IntegerField('Servings', validators=[InputRequired(), NumberRange(min=1)])
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    calories = FloatField('Calories', validators=[InputRequired()])
    total_fat = FloatField('Total Fat', validators=[InputRequired()])
    cholesterol = FloatField('Cholesterol', validators=[InputRequired()])
    sodium = FloatField('Sodium', validators=[InputRequired()])
    total_carbohydrates = FloatField('Total Carbohydrates', validators=[InputRequired()])
    protein = FloatField('Protein', validators=[InputRequired()])
    submit = SubmitField('Submit', validators=[InputRequired()])
    


class MealPlanForm(FlaskForm):
    timeFrame = StringField('Time Frame', validators=[InputRequired(), Length(min=1, max=255)])
    targetCalories = FloatField('Target Calories', validators=[InputRequired()])
    diet = StringField('Diet', validators=[InputRequired(), Length(min=1, max=255)])
    exclude = StringField('Exclude', validators=[Length(max=255)])
    submit = SubmitField('Submit')