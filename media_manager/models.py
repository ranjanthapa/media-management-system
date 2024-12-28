from django.db import models

class MediaFile(models.Model):
    name = models.CharField(max_length=255)
    size = models.IntegerField()  
    file = models.FileField(upload_to='uploads/')  
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name
