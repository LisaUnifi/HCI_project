from xml.dom import NotFoundErr
from django.db import models


class Album(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 20, blank=True, null=True)

    def __str__(self):
         return self.title



class ExifImage(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 20, blank=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to='exif/', blank=True, null=True)

