from datetime import datetime
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm, PasswordChangeForm
from .models import Mezzo, Missione, Scheda, TestaPiedi




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



class UserChangePass(PasswordChangeForm):
    
    
    def __init__(self, *args, **kwargs):
        super(UserChangePass, self).__init__(*args, **kwargs)
        
        self.fields['new_password1'].error_messages = {'required':'Nuova password richiesta!'}
        self.fields['new_password2'].error_messages = {'required':'Conferma password richiesta!'}
        self.fields['old_password'].error_messages = {'required':'Vecchia password richiesta!'}
        




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
    phone = forms.CharField(required=True,max_length=30, label='phone')

    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'corporation', 'email', 'phone']


    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].error_messages = {'required':'Username richiesto!'}
        self.fields['first_name'].error_messages = {'required':'Nome utente richiesto!'}
        self.fields['last_name'].error_messages = {'required':'Cognome utente richiesto!'}
        self.fields['password1'].error_messages = {'required':'Password richiesta!'}
        self.fields['password2'].error_messages = {'required':'Conferma password richiesta!'}
        self.fields['email'].error_messages = {'required':'Email richiesta!'}
        self.fields['phone'].error_messages = {'required':'Numero di cellulare richiesto!'}
        self.fields['corporation'].error_messages = {'required':'Associazione di appartenenza richiesa!'}


    def clean_username(self):
        '''
        Verify username is available.
        '''
        username = self.cleaned_data.get('username')
        qs = MyUser.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username già preso!")
        return username

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = MyUser.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Utente già registrato con questa mail!")
        return email

    def clean_password2(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("password2", "Le password devono essere uguali!")
        return password2

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        if len(password1) < 8 :
            self.add_error("password1", "La password deve contenere almeno 8 caratteri!")
        return cleaned_data


class MezziCreationForm(forms.ModelForm):
    """
        Creazione mezzi
    """

    class Meta:
        model = Mezzo
        fields = ['nome','tipologia','all_day','num_mezzo','equip_min']

    def __init__(self, *args, **kwargs):
        super(MezziCreationForm, self).__init__(*args, **kwargs)
        self.fields['nome'].error_messages = {'required':'Nome del mezzo richiesto!'}
        self.fields['tipologia'].error_messages = {'required':'Tipologia del mezzo richiesta!'}

    def clean_nome(self):
        '''
        Verify nome is available.
        '''
        nome = self.cleaned_data.get('nome')
        qs = Mezzo.objects.filter(nome=nome)
        if qs.exists():
            raise forms.ValidationError("Mezzo già in uso")
        return nome
        


class MissionCreationForm(forms.ModelForm):
    """
        Creazione missioni

        , 'invio'
    """

    class Meta:
        model = Missione
        fields = ['nome_p','cognome_p','luogo','patologia','criticita',
            'luogo_intervento', 'comune_intervento', 'cap_intervento', 'provincia_intervento', 
            'civico_intervento', 'cellulare', 'note', 'avvisi']

    def __init__(self, *args, **kwargs):
        super(MissionCreationForm, self).__init__(*args, **kwargs)
        self.fields['luogo'].error_messages = {'required':'Codice luogo richiesto!'}
        self.fields['patologia'].error_messages = {'required':'Codice patologia richiesta!'}
        self.fields['criticita'].error_messages = {'required':'Codice criticità richiesta!'}
        self.fields['luogo_intervento'].error_messages = {'required':'Luogo intervento richiesto!'}
        self.fields['comune_intervento'].error_messages = {'required':'Comune intervento richiesto!'}
        self.fields['cap_intervento'].error_messages = {'required':'CAP intervento richiesto!'}
        self.fields['civico_intervento'].error_messages = {'required':'Civico intervento richiesto!'}
        self.fields['provincia_intervento'].error_messages = {'required':'Provincia intervento richiesto!'}




class UserModificaForm(forms.ModelForm):
    """
    Registration Form
    """

    first_name = forms.CharField(required=True, max_length=30, label='first_name')
    last_name = forms.CharField(required=True, max_length=30, label='last_name')
    email = forms.EmailField(required=True, label='email')
    corporation = forms.CharField(max_length=30, required=True, label='corporation')
    phone = forms.CharField(required=True,max_length=30, label='phone')

    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'corporation', 'email', 'phone']

    def __init__(self, *args, **kwargs):
        super(UserModificaForm, self).__init__(*args, **kwargs)
        self.fields['username'].error_messages = {'required':'Username richiesto!'}
        self.fields['first_name'].error_messages = {'required':'Nome utente richiesto!'}
        self.fields['last_name'].error_messages = {'required':'Cognome utente richiesto!'}
        self.fields['email'].error_messages = {'required':'Email richiesta!'}
        self.fields['phone'].error_messages = {'required':'Numero di cellulare richiesto!'}
        self.fields['corporation'].error_messages = {'required':'Associazione di appartenenza richiesa!'}
        

    def clean_username(self):
            '''
            Verify username is available.
            '''
            username = self.cleaned_data.get('username')
            qs = MyUser.objects.filter(username=username)
            if qs.exists() and self.instance.username!=username:
                raise forms.ValidationError("Username già preso!")
            return username


class SchedaMissioneForm(forms.ModelForm):
    """
    Registration Form
    """

    class Meta:
        model = Scheda
        fields = [
            'scenario', 'cosciente','pervieta','ostruzione','dispnea','conto', 'respira', 'ascolto', 'palpo',
            'frequenza', 'saturazione', 'saturazione_oss', 'ossigeno', 'pressione_massima', 'pressione_minima',
            'temperatura', 'emorragie', 'polso', 'regolare_polso', 'cute', 'sudato', 'sudore_freddo', 'dolore_toracico', 'ora_dolore','data_dolore',
            'tipo_dolore', 'avpu', 'tempo', 'spazio', 'mimica_c', 'braccia_c', 'linguaggio_c', 'forza_sup',
            'forza_inf', 'sens_sup', 'sens_inf', 'posizione', 'allergie', 'patologie', 'glicemia', 'farmaci',
            'pasto', 'note', 'respiraBLS', 'circoloBLS', 'dae', 'cicli',
        ]

    '''
    def clean_testa_piedi(self):
            
            testa_piedi = self.instance.testa_piedi
            return testa_piedi
    '''
    


class MissioneModificaForm(forms.ModelForm):

    class Meta:
        model = Missione
        fields = [
            'nome_p', 'cognome_p',  'cellulare', 
            'data_nascita', 'dove_nato',
            'residenza', 'comune_residenza', 'civico_residenza', 'provincia_residenza', 'cap_residenza',
        ]



class MissioneTrasportoForm(forms.ModelForm):

    class Meta:
        model = Missione
        fields = [
            'criticita_trasporto','patologia_trasporto',
            'ospedale', 'reparto',
        ]

    criticita_trasporto = forms.CharField(required=True, label='criticita_trasporto')
    patologia_trasporto = forms.CharField(required=True, label='patologia_trasporto')
    ospedale = forms.CharField(required=True, label='ospedale')
    reparto = forms.CharField(required=True, label='reparto')

    def __init__(self, *args, **kwargs):
        super(MissioneTrasportoForm, self).__init__(*args, **kwargs)
        self.fields['criticita_trasporto'].error_messages = {'required':'Criticità richiesta!'}
        self.fields['patologia_trasporto'].error_messages = {'required':'Patologia richiesta!'}
        self.fields['ospedale'].error_messages = {'required':'Inserire ospedale di destinazione!'}
        self.fields['reparto'].error_messages = {'required':'Inserire reparto di destinazione!'}



class MissioneRifiutoForm(forms.ModelForm):

    class Meta:
        model = Missione
        fields = [
            'nome_t', 'cognome_t', 'parentela'
        ]

    nome_t = forms.CharField(required=True, label='nome_t')
    cognome_t = forms.CharField(required=True, label='cognome_t')
    parentela = forms.CharField(required=True, label='parentela')

    def __init__(self, *args, **kwargs):
        super(MissioneRifiutoForm, self).__init__(*args, **kwargs)
        self.fields['nome_t'].error_messages = {'required':'Nome del testimone richiesto!'}
        self.fields['cognome_t'].error_messages = {'required':'Cognome del testimone richiesto!'}
        self.fields['parentela'].error_messages = {'required':'Inserire grado di parentela!'}