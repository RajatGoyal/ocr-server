from supertramp_server.settings import MEDIA_ROOT
from django.db import models

# Create your models here.

class Details(models.Model):
    image = models.ImageField(upload_to=MEDIA_ROOT)
    result = models.TextField()

    class Meta:
        db_table = 'ocr_details'