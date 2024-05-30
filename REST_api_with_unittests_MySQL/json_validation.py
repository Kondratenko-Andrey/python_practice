from marshmallow import Schema, fields


# Определение схемы JSON для валидации
class TaskSchemaPOST(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=False)


class TaskSchemaGET(Schema):
    title = fields.Str(required=False)
    description = fields.Str(required=False)
