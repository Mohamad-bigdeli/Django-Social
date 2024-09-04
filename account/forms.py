from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=250, required=True, label="Username or Phone",
                            widget=forms.TextInput())
    password = forms.CharField(max_length=250, required=True, label="Password",
                            widget=forms.PasswordInput())
    
class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput, label="password")
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput, label="repeat password")

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'phone', 'email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError("UsernameIsExists")
        return username
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError("PhoneIsExists")
        return phone    

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise forms.ValidationError("UsernameIsExists")
        return email       

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")        
        return password2
    
class EditUserForm(forms.ModelForm):
     
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'date_of_birth', 'job', 'bio', 'email', 'photo']   

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super(EditUserForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        for field in self.fields:
            if not cleaned_data.get(field):
                cleaned_data[field] = getattr(self.instance, field)
        return cleaned_data
    
   
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise forms.ValidationError("UsernameIsExists")
        return email  
    
    
class ForgetPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError("Your email is not registered, please register it")
    
class PasswordResetConfirmForm(forms.Form):
    password1 = forms.CharField(max_length=15, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=15, widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 == password2:
            return password2
        raise forms.ValidationError("Passwords do not match")
        



        