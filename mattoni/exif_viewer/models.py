from django.db import models


class Album(models.Model):
    id = models.IntegerField(primary_key = True, default=1000)
    title = models.CharField(max_length = 50, blank=True, null=True)

    def __str__(self):
         return self.title



class ExifImage(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 120, blank=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to='exif/', blank=True, null=True)

