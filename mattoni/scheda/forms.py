from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
from .models import Mezzo, Missione

MyUser = get_user_model()

class RegisterForm(forms.ModelForm):
    """
    The default 

    """

    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    email = forms.EmailField(widget=forms.EmailInput)

    class Meta:
        model = MyUser
        fields = ['username']

    def clean_username(self):
        '''
        Verify username is available.
        '''
        username = self.cleaned_data.get('username')
        qs = MyUser.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("username is taken")
        return username

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = MyUser.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['username']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ['username', 'password', 'is_active', 'admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserRegistrationForm(UserCreationForm):
    """
    Registration Form
    """


    first_name = forms.CharField(required=True, max_length=30, label='first_name')
    last_name = forms.CharField(required=True, max_length=30, label='last_name')
    password1 = forms.CharField(required=True, label='password1')
    password2 = forms.CharField(required=True, label='password2')
    email = forms.EmailField(required=True, label='email')
    corporation = forms.CharField(max_length=30, required=True, label='corporation')
    phone = forms.CharField(max_length=30, label='phone')
    user_type = forms.CharField(max_length=30, label='user_type')

    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'corporation', 'email', 'phone']


    def clean_username(self):
        '''
        Verify username is available.
        '''
        username = self.cleaned_data.get('username')
        qs = MyUser.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("username is taken")
        return username

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = MyUser.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email


    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

class MezziCreationForm(forms.ModelForm):
    """
        Creazione mezzi
    """

    class Meta:
        model = Mezzo
        fields = ['nome','tipologia','all_day','num_mezzo','equip_min']

class MissionCreationForm(forms.ModelForm):
    """
        Creazione missioni
    """

    class Meta:
        model = Missione
        fields = ['nome_p','cognome_p','luogo','patologia','criticita',
            'luogo_intervento', 'comune_intervento', 'cap_intervento', 'provincia_intervento', 
            'civico_intervento', 'cellulare', 'note', 'avvisi']
