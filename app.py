from flask import Flask, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from comment.crud import CommentView
from database import Base, engine, session
from recipie.models import Recipe
from recipie.crud import recipes_schema, RecipeAPI
from user.models import User
from utils import generate_access_token, generate_refresh_token, SECRET_KEY
from wishlist.crud import WishlistView

app = Flask(__name__)

Base.metadata.create_all(engine)
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = SECRET_KEY
jwt = JWTManager(app)


app.add_url_rule('/recipe/<int:recipe_id>', view_func=RecipeAPI.as_view('recipe'))
app.add_url_rule('/recipe', view_func=RecipeAPI.as_view('create_recipe'), methods=['POST'])
app.add_url_rule('/recipe/<int:recipe_id>', view_func=RecipeAPI.as_view('update_recipe'), methods=['PUT'])
app.add_url_rule('/recipe/<int:recipe_id>', view_func=RecipeAPI.as_view('delete_recipe'), methods=['DELETE'])

wishlist_view = WishlistView.as_view('wishlist_api')
app.add_url_rule('/wishlist', view_func=wishlist_view, methods=['GET', 'POST'])
app.add_url_rule('/wishlist/<int:wishlist_id>', view_func=wishlist_view, methods=['GET', 'DELETE'])

comment_view = CommentView.as_view('comment_api')
app.add_url_rule('/comment', view_func=comment_view, methods=['POST'])
app.add_url_rule('/comment/<int:comment_id>', view_func=comment_view, methods=['DELETE', 'PUT'])
app.add_url_rule('/get_comment/<int:recipe_id>', view_func=comment_view, methods=['GET'])


@app.route('/user', methods=['POST'])
def create_user():
    """
    Create user api
    :params:
        email(str): unique email id
        password(str): password set by the user
    :return:
        User successfully created(200 ok)
        User already exist(409)
    """
    email = request.json['email']
    password = request.json['password']
    user = session.query(User).filter_by(email=email).first()
    if user:
        return {'message': f'User with email the already exist.'}, 409
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(email=email, password=hashed_password)
    session.add(user)
    session.commit()

    return {'message': f'User {email} created successfully.'}, 201


@app.route('/login', methods=['POST'])
def login():
    """
    User login api
    params:
        email(str): unique email id
        password(str): password set by the user
    :return:
        User successfully loggedin(200 ok)
        Invalid email or password(401)
    """
    email = request.json['email']
    password = request.json['password']

    user = session.query(User).filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return {'message': 'Invalid email or password'}, 401

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    return {
        'message': 'Logged in successfully',
        'access_token': access_token,
        'refresh_token': refresh_token
    }


@app.route('/recipes')
@jwt_required()
def get_recipes():
    """
    Api to return all recipies
    :return:
        List of recipies
    """
    recipes = session.query(Recipe).all()
    return recipes_schema.dump(recipes)


# GET all recipe
@app.route('/recipes/current_user')
@jwt_required()
def get_current_user_recipes():
    """
    Api to return all recipies added by the loggedin user
    :return:
        List of recipies
    """
    current_user = get_jwt_identity()
    recipes = session.query(Recipe).filter_by(user_id=current_user)
    return recipes_schema.dump(recipes)


@app.route('/search')
def recipe_search():
    """
    Api to return recipies based on a keyword
    :params:
        keyword(str): Keyword for searching
    :return:
        List of recipies
    """
    keyword = request.args.get('keyword', '')
    recipes = session.query(Recipe).filter(Recipe.name.like(f'%{keyword}%') | Recipe.description.like(f'%{keyword}%'))
    return recipes_schema.dump(recipes)
