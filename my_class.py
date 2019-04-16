from pymodm import MongoModel, fields


class User(MongoModel):
    user_name = fields.CharField(primary_key=True)
    processing_type = fields.CharField()
    time_uploaded = fields.CharField()
    time_to_process = fields.CharField()
    image_size = fields.IntegerField()
