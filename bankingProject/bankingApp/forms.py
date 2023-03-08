from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import User



class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True,max_length=255, help_text="Required", widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address',} ))
    username = forms.CharField(label='Username', max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Enter a username',}))
    first_name=forms.CharField(label='fname', max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Enter your firstname',}))
    last_name=forms.CharField(label='sname', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter your  surname',}))
    password1 = forms.CharField(label='Password1', max_length=100,widget=forms.PasswordInput(attrs={'placeholder': 'Enter a password',}))
    password2 = forms.CharField(label='Password2', max_length=100,widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter your password', }))

    class Meta:
        model = User
        fields = ("first_name","last_name","username","email","password1","password2",)


    
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }