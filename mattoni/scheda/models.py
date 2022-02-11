from django.db import models
import datetime
from django.utils import timezone 
from django.contrib.auth.models import AbstractUser, BaseUserManager
from PIL import Image



class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=self.normalize_email(username),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            username=username,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username=username,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


#custom User class for authentication
class MyUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True,
        help_text= ('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'))
    #also has first_name and last_name
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    is_operator = models.BooleanField(default=False)
    corporation = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


class Scheda(models.Model):
    id_scheda = models.AutoField(primary_key = True)

    scenario = models.CharField(max_length = 20)

    cosciente = models.BooleanField()
    respiraBLS = models.BooleanField()
    circoloBLS = models.BooleanField()
    dae = models.BooleanField()
    cicli = models.IntegerField(default = 0)
    noteBLS = models.TextField()
    pervieta = models.BooleanField()
    ostruzione = models.BooleanField()

    dispnea = models.BooleanField()
    osservo = models.CharField(max_length = 20)
    palpo = models.CharField(max_length = 20)
    ascolto = models.BooleanField()
    conto = models.IntegerField()
    saturazione = models.IntegerField()
    saturazione_oss = models.IntegerField()
    ossigeno = models.IntegerField()

    pressione_massima = models.IntegerField()
    pressione_minima = models.IntegerField()
    temperatura = models.IntegerField()
    emorragie = models.CharField(max_length = 20)
    polso = models.BooleanField()
    regolare_polso = models.BooleanField()
    cute = models.CharField(max_length = 20)
    sudato = models.BooleanField()
    dolore_toracico = models.BooleanField()
    ora_dolore = models.DateTimeField(auto_now = False, auto_now_add = False)
    tipo_dolore = models.BooleanField()

    avpu = models.CharField(max_length = 1)
    tempo = models.BooleanField()
    spazio = models.BooleanField()
    mimica_c = models.CharField(max_length = 10)
    braccia_c = models.CharField(max_length = 10)
    linguaggio_c = models.BooleanField()
    forza_sup = models.CharField(max_length = 10)
    forza_inf = models.CharField(max_length = 10)
    sens_sup = models.CharField(max_length = 10)
    sens_inf = models.CharField(max_length = 10)

    posizione = models.CharField(max_length = 20)
    allergie = models.TextField()
    patologie = models.TextField()
    glicemia = models.IntegerField()
    farmaci = models.TextField()
    pasto = models.TextField()
    #setta immagini 
    testa_piedi_front = models.ImageField(upload_to = '')
    testa_piedi_back = models.ImageField(upload_to = '')

    note = models.TextField()


class Mezzo(models.Model):
    id_mezzo = models.AutoField(primary_key = True)
    nome = models.CharField(unique = True, max_length = 10)
    tipologia = models.CharField(max_length = 10)
    all_day = models.BooleanField(default = False)
    username = models.ForeignKey(MyUser, on_delete = models.CASCADE)
    num_mezzo = models.IntegerField()
    equip_min = models.IntegerField()


class Missione(models.Model):
    id_missione = models.AutoField(primary_key = True)
    luogo = models.CharField(max_length = 1)
    patologia = models.IntegerField()
    criticita = models.CharField(max_length = 1)
    nome_p = models.CharField(max_length = 20, blank=True,null=True)
    cognome_p = models.CharField(max_length = 20, default = "NON DEFINITO")
    luogo_intervento = models.CharField(max_length = 100)
    civico_intervento = models.CharField(max_length = 5)
    comune_intervento = models.CharField(max_length = 20)
    provincia_intervento = models.CharField(max_length = 2)
    cap_intervento = models.IntegerField()
    cellulare = models.CharField(max_length = 15, blank=True,null=True)
    note = models.TextField(blank=True)
    avvisi = models.TextField(blank=True)

    data_nascita = models.DateField(blank=True ,null=True)
    dove_nato = models.CharField(max_length = 25, blank=True,null=True)
    eta = models.IntegerField(blank=True,null=True)
    residenza = models.CharField(max_length = 100, blank=True,null=True)
    comune_residenza = models.CharField(max_length = 20, blank=True,null=True)
    civico_residenza = models.CharField(max_length = 5, blank=True,null=True)
    provincia_residenza = models.CharField(max_length = 2, blank=True,null=True)
    cap_residenza = models.IntegerField(blank=True,null=True)

    invio = models.DateTimeField(auto_now_add = True)
    inizio = models.DateTimeField(blank=True, null=True)
    arrivo = models.DateTimeField(blank=True,null=True)
    partenza = models.DateTimeField(blank=True,null=True)
    pronto_socc = models.DateTimeField(blank=True,null=True)
    fine = models.DateTimeField(blank=True,null=True)
    sede = models.DateTimeField(blank=True,null=True)

    #capire come gestire esito
    esito = models.CharField(max_length = 20, blank=True,null=True)
    
    #chiusa = models.BooleanField(default = False)


class Intervento(models.Model):
    id_scheda = models.OneToOneField(Scheda, on_delete = models.CASCADE)
    id_mezzo = models.OneToOneField(Mezzo, on_delete = models.CASCADE)
    id_missione = models.OneToOneField(Missione, on_delete = models.CASCADE)

