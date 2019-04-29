from pymodm import MongoModel, fields


class User(MongoModel):
    user_name = fields.CharField(primary_key=True)
    file_name = fields.ListField()
    original_image = fields.ListField()
    processing_type = fields.ListField()
    image_display = fields.CharField()
    processed_image = fields.ListField()
    time_uploaded = fields.CharField()
    time_to_process = fields.CharField()
    image_size = fields.IntegerField()
    image_format = fields.CharField()
