from pymodm import MongoModel, fields


class User(MongoModel):
    user_name = fields.CharField(primary_key=True)
    #original_image = fields.ImageField()
    processing_type = fields.ListField()
    image_display= fields.CharField()
    #processed_image =
    time_uploaded = fields.CharField()
    time_to_process = fields.CharField()
    image_size = fields.IntegerField()
