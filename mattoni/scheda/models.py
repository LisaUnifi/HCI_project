from django.db import models
import datetime
from django.utils import timezone 
from django.contrib.auth.models import AbstractUser

#custom User class for authentication
class MyUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True,
        help_text= ('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        error_messages={
            'unique': ("A user with that username already exists."),
        })
    first_name = models.CharField(('first name'), max_length=30, blank=True)
    last_name = models.CharField(('last name'), max_length=30, blank=True)
    email = models.EmailField(('email address'), blank=True)
    is_active = models.BooleanField(('active'), default=True,
        help_text=('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(('date joined'), default=timezone.now)
    is_staff = models.BooleanField(('staff status'), default=False,
        help_text=('Designates whether the user can log into this admin '
                    'site.'))
    is_operator = models.BooleanField(('operator status'), default=False,
        help_text=('Designates whether the user is an operator type user or not.'))


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    example = models.IntegerField(default = 7)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)