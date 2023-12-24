from tortoise import fields, Model


class User(Model):
    """
    User Tortoise database model
    """

    class Meta:
        table = "users"
        app = "users"

    id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=128, unique=True)
    first_name = fields.CharField(max_length=128)
    last_name = fields.CharField(max_length=128)
    password = fields.CharField(max_length=128)
    phone_number = fields.CharField(max_length=128, null=True)
    email = fields.CharField(max_length=128, null=True)
    active = fields.BooleanField(default=True, null=True)
    display_name = fields.CharField(max_length=255, null=True)
    search_field = fields.CharField(max_length=255, null=True)
