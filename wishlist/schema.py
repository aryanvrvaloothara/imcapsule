from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from recipie.schema import RecipeSchema
from user.schema import UserSchema
from wishlist.models import Wishlist


class WishlistSchema(SQLAlchemyAutoSchema):
    recipe = fields.Nested(RecipeSchema)
    user = fields.Nested(UserSchema)

    class Meta:
        model = Wishlist
        load_instance = True


wishlist_schema = WishlistSchema()
wishlists_schema = WishlistSchema(many=True)