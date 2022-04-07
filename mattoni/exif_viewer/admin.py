from django.contrib import admin

from .models import ExifImage, Album


class ExifImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','album','note','img')

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(Album, AlbumAdmin)
admin.site.register(ExifImage, ExifImageAdmin)