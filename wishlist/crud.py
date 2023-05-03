from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from database import session
from wishlist.models import Wishlist
from wishlist.schema import wishlist_schema, wishlists_schema


class WishlistView(MethodView):
    decorators = [jwt_required()]

    def get(self):
        current_user = get_jwt_identity()
        wishlist = session.query(Wishlist).filter_by(user_id=current_user)
        if wishlist:
            return wishlists_schema.dump(wishlist)
        else:
            return jsonify({'error': 'Wishlist item not found'}), 404

    def post(self):
        current_user = get_jwt_identity()
        data = request.json
        data['user_id'] = current_user
        wishlist = Wishlist(**data)
        session.add(wishlist)
        session.commit()
        return wishlist_schema.dump(wishlist), 201

    def delete(self, wishlist_id):
        wishlist = session.query(Wishlist).get(wishlist_id)
        if wishlist:
            session.delete(wishlist)
            session.commit()
            return jsonify({'message': 'Wishlist item deleted'})
        else:
            return jsonify({'error': 'Wishlist item not found'}), 404

    def get_all(self):
        current_user = get_jwt_identity()
        wishlists = session.query(Wishlist).filter_by(user_id=current_user)
        return wishlists_schema.dump(wishlists)