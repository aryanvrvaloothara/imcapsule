from marshmallow import Schema, fields


class RecipeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)


recipie_schema = RecipeSchema()
recipies_schema = RecipeSchema(many=True)