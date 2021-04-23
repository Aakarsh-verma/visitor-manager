from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import Society

class CreateSocietyForm(ModelForm):
    class Meta:
        model = Society
        fields = ['name', 'sec_name', 'address', 'user']

        widgets = {
            'user' : forms.TextInput(attrs={'readonly': 'readonly'})
        }

class EditSocietyInfoForm(ModelForm):
    class Meta:
        model   = Society
        fields  = ['name', 'sec_name']

class CreateUserForm(UserCreationForm):
    class Meta:
        model   = User
        fields  = ['username', 'email', 'password1', 'password2']

# class UserUpdateForm(UserChangeForm):
#     class Meta:
#         model   = User
#         fields  = ['username', 'email']