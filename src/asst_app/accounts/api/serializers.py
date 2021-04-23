from rest_framework import serializers

from django.contrib.auth.models import User

from accounts.models import Society, ValidVisitor


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style = {'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only':True}
        }
    
    def save(self):
        user = User(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match!'})
        user.set_password(password)
        user.save()
        return user

class SocietySerializer(serializers.ModelSerializer):
    class Meta:
        model = Society
        fields = ['id', 'name', 'sec_name', 'address']



class ValidVisitorSerializer(serializers.ModelSerializer):
    
    secretary = serializers.SerializerMethodField('get_society_name')
    
    class Meta:
        model = ValidVisitor
        fields = ['id', 'name', 'entry_date', 'entry_time', 'temp']
    
    def get_society_name(self, visitor):
        secretary = visitor.soc_name.sec_name
        return secretary