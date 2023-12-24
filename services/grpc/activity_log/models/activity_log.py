from tortoise import fields, Model


class Message(Model):
    """
    User Tortoise database model
    """

    class Meta:
        table = "activity_log"
        app = "activity_log"

    id = fields.UUIDField(pk=True)
    description = fields.CharField(max_length=128)
