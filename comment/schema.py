from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from comment.models import Comment
from user.schema import UserSchema


class CommentSchema(SQLAlchemyAutoSchema):
    user = fields.Nested(UserSchema)

    class Meta:
        model = Comment
        load_instance = True


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)