from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm, MezziCreationForm
from .models import Mezzo, Missione, Scheda, Intervento, TestaPiedi

MyUser = get_user_model()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['username', 'admin','corporation','phone', 'first_name', 'last_name', 'is_active', 'staff', 'email']
    list_filter = ['admin']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin','staff','is_operator',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password','password_2')}
        ),
    )
    search_fields = ['username']
    ordering = ['username']
    filter_horizontal = ()


class MezzoAdmin(admin.ModelAdmin):
    list_display = ('id_mezzo', 'nome','tipologia','all_day','num_mezzo','equip_min', 'username')
    

class MissioneAdmin(admin.ModelAdmin):
    list_display = (
        'id_missione',
        'luogo', 'patologia', 'criticita',
        'nome_p', 'cognome_p', 'luogo_intervento', 'civico_intervento', 'comune_intervento', 'provincia_intervento', 'cap_intervento', 'cellulare', 'note', 'avvisi',
        'data_nascita', 'dove_nato', 'residenza', 'comune_residenza', 'civico_residenza', 'provincia_residenza', 'cap_residenza', 
        'invio', 'accetta_missione', 'partenza', 'arrivo', 'conferma_trasporto', 'rifiuto_trasporto', 'pronto_socc', 'libero', 'rientro_sede', 
        'criticita_trasporto', 'patologia_trasporto', 'ospedale', 'reparto', 
        'nome_t', 'cognome_t', 'parentela',
        'esito', 'chiusa'
        )


class TestaPiediAdmin(admin.ModelAdmin):
    list_display = ('id_testa_piedi', 'front', 'back')


class SchedaAdmin(admin.ModelAdmin):
    list_display = (
        'id_scheda', 'scenario', 'cosciente', 'respiraBLS', 'circoloBLS', 'dae', 'cicli', 'pervieta', 'ostruzione', 
        'respira', 'dispnea', 'palpo', 'ascolto', 'conto', 'saturazione', 'saturazione_oss', 'ossigeno', 
        'pressione_massima', 'pressione_minima', 'frequenza', 'temperatura', 'emorragie', 'polso', 'regolare_polso', 'cute', 'sudato', 'sudore_freddo', 'dolore_toracico', 'ora_dolore', 'data_dolore', 'tipo_dolore', 
        'avpu', 'tempo', 'spazio', 'mimica_c', 'braccia_c', 'linguaggio_c', 'forza_sup', 'forza_inf', 'sens_sup', 'sens_inf', 
        'posizione', 'allergie', 'patologie', 'glicemia', 'farmaci', 'pasto', 'testa_piedi', 
        'note'
        )


class InterventoAdmin(admin.ModelAdmin):
    list_display = ('id_scheda','id_mezzo','id_missione')


admin.site.register(MyUser, UserAdmin)
admin.site.register(Mezzo, MezzoAdmin)
admin.site.register(Missione, MissioneAdmin)
admin.site.register(TestaPiedi, TestaPiediAdmin)
admin.site.register(Scheda, SchedaAdmin)
admin.site.register(Intervento, InterventoAdmin)