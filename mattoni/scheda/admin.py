from django.contrib import admin
from .models import Question, Choice

from scheda.models import MyUser

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

@admin.register(MyUser)
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)