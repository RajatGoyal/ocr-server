from django.db import models

# Create your models here.

class Details(models.Model):
    image = models.ImageField()
    result = models.TextField()

    class Meta:
        db_table = 'ocr_details'