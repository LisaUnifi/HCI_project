from rest_framework import serializers
from scheda.models import MyUser

#TODO: sarebbe da creare alcune views per testare la serializzazione
class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_active','date_joined','is_staff','is_operator']


#vecchia versione
'''
class MyUserSerializer(serializers.Serializers):
    id = serializers.AutoField(max_length=30, required=True)
    username = serializers.CharField(max_length=30)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    is_active = serializers.BooleanField()
    date_joined = serializers.DateTimeField()
    is_staff = serializers.BooleanField()
    is_operator = serializers.BooleanField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return MyUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.id =validated_data.get('id', instance.id)
        instance.username =validated_data.get('username', instance.username)
        instance.first_name =validated_data.get('first_name', instance.first_name)
        instance.last_name =validated_data.get('last_name', instance.last_name)
        instance.email =validated_data.get('email', instance.email)
        instance.is_active =validated_data.get('is_active', instance.is_active)
        instance.date_joined =validated_data.get('date_joined', instance.date_joined)
        instance.is_staff =validated_data.get('is_staff', instance.is_staff)
        instance.is_operator =validated_data.get('is_operator', instance.is_operator)

        instance.save()
        return instance
'''