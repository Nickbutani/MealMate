
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt



db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)
    



class User(db.Model):
    
    __tablename__ = 'user'
    
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    @classmethod
    def serialize(cls):
        return {
            'user_id': cls.user_id,
            'username': cls.username,
            'email': cls.email,
            'password': cls.password
        }
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        password_str = password.decode('utf-8')
        user = cls(username=username, password=password_str, email=email, first_name=first_name, last_name=last_name)
        db.session.add(user)
        return user

            
    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user
        else:
            return False

class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    
    # recipe information
    title = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255))
    source_name = db.Column(db.String(255))
    source_url = db.Column(db.String(255))
    servings = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('recipes', lazy=True))
    
    # Ingredients
    ingredients = db.Column(db.JSON)  
    
    
    # Nutritional Information
    calories = db.Column(db.Float)
    total_fat = db.Column(db.Float)
    cholesterol = db.Column(db.Float)
    sodium = db.Column(db.Float)
    total_carbohydrates = db.Column(db.Float)
    protein = db.Column(db.Float)
    
    
