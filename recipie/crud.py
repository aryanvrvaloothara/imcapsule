from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from database import session
from recipie.models import Recipe
from recipie.schema import RecipeSchema


recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)


class RecipeAPI(MethodView):
    decorators = [jwt_required()]

    def get(self, recipe_id):
        """
        Api to return single recipe
        :params:
            recipe_id(int): Id for retrieving recipe
        :return:
            recipe details
        """
        recipe = session.query(Recipe).get(recipe_id)
        if recipe:
            return recipe_schema.dump(recipe)
        else:
            return jsonify({'error': 'Recipe not found'}), 404

    def post(self):
        """
        Api create a recipe
        :params:
            name(str): recipe name
            description(str): recipe description
        :return:
            recipe details
        """
        current_user = get_jwt_identity()
        data = request.json
        data['user_id'] = current_user
        recipe = Recipe(**data)
        session.add(recipe)
        session.commit()
        return recipe_schema.dump(recipe)

    # PUT (update) an existing recipe
    def put(self, recipe_id):
        """
        Api create a recipe
        :params:
            recipe_id(int): recipie id
            name(str): recipe name
            description(str): recipe description
        :return:
            recipe details
        """
        recipe = session.query(Recipe).get(recipe_id)
        if recipe:
            recipe.name = request.json['name']
            recipe.description = request.json['description']
            session.commit()
            return recipe_schema.dump(recipe)
        else:
            return jsonify({'error': 'recipe not found'}), 404

    # DELETE a recipe
    def delete(self, recipe_id):
        """
        Api create a recipe
        :params:
            recipe_id(int): recipie id
        :return:
            Recipe not found(404)
            Recipe deleted(200)
        """
        recipe = session.query(Recipe).get(recipe_id)
        if recipe:
            session.delete(recipe)
            session.commit()
            return jsonify({'message': 'Recipe deleted'})
        else:
            return jsonify({'error': 'Recipe not found'}), 404

