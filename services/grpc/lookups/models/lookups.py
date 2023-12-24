from tortoise import fields, Model


class Lookups(Model):
    """
    User Tortoise database model
    """

    class Meta:
        table = "lookups"
        app = "lookups"

    id = fields.UUIDField(pk=True)
    code = fields.CharField(max_length=32, unique=True)
    service = fields.CharField(max_length=128)
