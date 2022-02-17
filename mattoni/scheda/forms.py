from datetime import datetime
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
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
    """

    class Meta:
        model = Missione
        fields = ['nome_p','cognome_p','luogo','patologia','criticita',
            'luogo_intervento', 'comune_intervento', 'cap_intervento', 'provincia_intervento', 
            'civico_intervento', 'cellulare', 'note', 'avvisi']


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
            'temperatura', 'emorragie', 'polso', 'regolare_polso', 'cute', 'sudato', 'dolore_toracico', 'ora_dolore',
            'tipo_dolore', 'avpu', 'tempo', 'spazio', 'mimica_c', 'braccia_c', 'linguaggio_c', 'forza_sup',
            'forza_inf', 'sens_sup', 'sens_inf', 'posizione', 'allergie', 'patologie', 'glicemia', 'farmaci',
            'pasto', 'note'
        ]

    '''
    def clean_testa_piedi(self):
            
            testa_piedi = self.instance.testa_piedi
            return testa_piedi
    '''
        

    def clean_cosciente(self):
            '''
            Set cosciente to True or False
            '''
            data = self.cleaned_data.get('cosciente')
            if data == 'True':
                cosciente = True
            elif data == 'False':
                cosciente = False
            else:
                cosciente = None
            return cosciente

    def clean_pervieta(self):
            '''
            Set pervieta to True or False
            '''
            data = self.cleaned_data.get('pervieta')
            if data == 'True':
                pervieta = True
            elif data == 'False':
                pervieta = False
            else:
                pervieta = None
            return pervieta

    def clean_ostruzione(self):
            '''
            Set ostruzione to True or False
            '''
            data = self.cleaned_data.get('ostruzione')
            if data == 'True':
                ostruzione = True
            elif data == 'False':
                ostruzione = False
            else:
                ostruzione = None
            return ostruzione


    def clean_dispnea(self):
            '''
            Set dispnea to True or False
            '''
            data = self.cleaned_data.get('dispnea')
            if data == 'True':
                dispnea = True
            elif data == 'False':
                dispnea = False
            else:
                dispnea = None
            return dispnea

    def clean_respira(self):
            '''
            Set respira to True or False
            '''
            data = self.cleaned_data.get('respira')
            if data == 'True':
                respira = True
            elif data == 'False':
                respira = False
            else:
                respira = None
            return respira

    def clean_ascolto(self):
            '''
            Set ascolto to True or False
            '''
            data = self.cleaned_data.get('ascolto')
            if data == 'True':
                ascolto = True
            elif data == 'False':
                ascolto = False
            else:
                ascolto = None
            return ascolto

    def clean_emorragie(self):
            '''
            Set emorragie to True or False
            '''
            data = self.cleaned_data.get('emorragie')
            if data == 'True':
                emorragie = True
            elif data == 'False':
                emorragie = False
            else:
                emorragie = None
            return emorragie


    def clean_polso(self):
            '''
            Set polso to True or False
            '''
            data = self.cleaned_data.get('polso')
            if data == 'True':
                polso = True
            elif data == 'False':
                polso = False
            else:
                polso = None
            return polso


    def clean_regolare_polso(self):
            '''
            Set regolare_polso to True or False
            '''
            data = self.cleaned_data.get('regolare_polso')
            if data == 'True':
                regolare_polso = True
            elif data == 'False':
                regolare_polso = False
            else:
                regolare_polso = None
            return regolare_polso


    def clean_sudato(self):
            '''
            Set sudato to True or False
            '''
            data = self.cleaned_data.get('sudato')
            if data == 'True':
                sudato = True
            elif data == 'False':
                sudato = False
            else:
                sudato = None
            return sudato
    

    def clean_dolore_toracico(self):
            '''
            Set dolore_toracico to True or False
            '''
            data = self.cleaned_data.get('dolore_toracico')
            if data == 'True':
                dolore_toracico = True
            elif data == 'False':
                dolore_toracico = False
            else:
                dolore_toracico = None
            return dolore_toracico


    def clean_ora_dolore(self):
            '''
            Set ora_dolore to DateTimeField
            '''
            ora = self.cleaned_data.get('ora_dolore')
            data = self.cleaned_data.get('data_dolore')
            if ora == None and data == None:
                ora_dolore = None
            elif data == None:
                d = datetime.now().date()
                h = datetime.strptime(ora,'%H:%M').time()
                ora_dolore = datetime.combine(d,h)
            else:
                d = datetime.strptime(data,'%m/%d/%Y').date()
                h = datetime.strptime(ora,'%H:%M').time()
                ora_dolore = datetime.combine(d,h)
            return ora_dolore

    
    def clean_tipo_dolore(self):
            '''
            Set tipo_dolore to True or False
            '''
            data = self.cleaned_data.get('tipo_dolore')
            if data == 'True':
                tipo_dolore = True
            elif data == 'False':
                tipo_dolore = False
            else:
                tipo_dolore = None
            return tipo_dolore
    

    def clean_tempo(self):
            '''
            Set tempo to True or False
            '''
            data = self.cleaned_data.get('tempo')
            if data == 'True':
                tempo = True
            elif data == 'False':
                tempo = False
            else:
                tempo = None
            return tempo


    def clean_spazio(self):
            '''
            Set spazio to True or False
            '''
            data = self.cleaned_data.get('spazio')
            if data == 'True':
                spazio = True
            elif data == 'False':
                spazio = False
            else:
                spazio = None
            return spazio


    def clean_linguaggio_c(self):
            '''
            Set linguaggio_c to True or False
            '''
            data = self.cleaned_data.get('linguaggio_c')
            if data == 'True':
                linguaggio_c = True
            elif data == 'False':
                linguaggio_c = False
            else:
                linguaggio_c = None
            return linguaggio_c