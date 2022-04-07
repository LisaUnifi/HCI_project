
from django import forms
from .models import ExifImage, Album


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title']

    title = forms.CharField(required=True, label='title')
    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['title'].error_messages = {'required':'Nome del nuovo album richiesto!'}


class ExifForm(forms.ModelForm):

    class Meta:
        model = ExifImage
        fields = ['name', 'note', 'img']

    name = forms.CharField(required=True, label='name')
    img = forms.ImageField(required=True, label='img')

    def __init__(self, *args, **kwargs):
        super(ExifForm, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages = {'required':'Nome immagine richiesto!'}
        self.fields['img'].error_messages = {'required':'Seleziona una immagine!'}


class MapsForm(forms.Form):
    map = forms.CharField(required=True, label='map')

    latitude = forms.CharField(label='latitude')
    longitude = forms.CharField(label='longitude')

    zoom = forms.CharField(empty_value='15', label='zoom')
    basemap = forms.CharField(empty_value='roadmap', label='basemap')
    layer = forms.CharField(empty_value='none', label='layer')

    pitch = forms.CharField(empty_value='35', label='pitch')
    fov = forms.CharField(empty_value='80', label='fov')