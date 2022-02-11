from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm, MezziCreationForm
from .models import Mezzo, Missione, Scheda, Intervento

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
    list_display = ('nome','tipologia','all_day','num_mezzo','equip_min', 'username')
    
class MissioneAdmin(admin.ModelAdmin):
    list_display = ('nome_p','cognome_p','luogo','patologia','criticita',
            'luogo_intervento', 'comune_intervento', 'cap_intervento', 'provincia_intervento', 
            'civico_intervento', 'cellulare', 'note', 'avvisi')

class SchedaAdmin(admin.ModelAdmin):
    list_display = ('id_scheda','scenario')

class InterventoAdmin(admin.ModelAdmin):
    list_display = ('id_scheda','id_mezzo','id_missione')


admin.site.register(MyUser, UserAdmin)
admin.site.register(Mezzo, MezzoAdmin)
admin.site.register(Missione, MissioneAdmin)
admin.site.register(Scheda, SchedaAdmin)
admin.site.register(Intervento, InterventoAdmin)