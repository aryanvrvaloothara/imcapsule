from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from comment.models import Comment
from comment.schema import comments_schema, comment_schema
from database import session
from recipie.models import Recipe


class CommentView(MethodView):
    decorators = [jwt_required()]

    def get(self, recipe_id):
        """
        Api to get all comment of a recipie
        :params:
            recipe_id(int): recipe id
        :return:
            Coment details
            Comment not found(404)
        """
        comments = session.query(Comment).filter_by(recipe_id=recipe_id)
        if comments:
            return comments_schema.dump(comments)
        else:
            return jsonify({'error': 'Comment not found'}), 404

    def post(self):
        """
        Api to add a comment
        :params:
            recipe_id(int): recipe id
            body(str): comment description
        :return:
            Comment deleted(200)
            Comment not found(404)
        """
        current_user = get_jwt_identity()
        data = request.json
        data['user_id'] = current_user
        recipe = session.query(Recipe).get(data['recipe_id'])
        if not recipe:
            return jsonify({'error': 'Invalid recipe id'}), 404
        comment = Comment(**data)
        session.add(comment)
        session.commit()
        return comment_schema.dump(comment), 201

    def delete(self, comment_id):
        """
        Api to delete a comment
        :params:
            comment_id(int): comment id
            body(str): comment description
        :return:
            Comment deleted(200)
            Comment not found(404)
        """
        comment = session.query(Comment).get(comment_id)
        if comment:
            session.delete(comment)
            session.commit()
            return jsonify({'message': 'Comment deleted'})
        else:
            return jsonify({'error': 'Comment not found'}), 404

    def put(self, comment_id):
        """
        Api to update a comment
        :params:
            comment_id(int): comment id
            body(str): comment description
        :return:
            comment details
        """
        comment = session.query(Comment).get(comment_id)
        if comment:
            comment.body = request.json['body']
            session.commit()
            return comment_schema.dump(comment)
        else:
            return jsonify({'error': 'comment not found'}), 404
