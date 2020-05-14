from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import *
from posts.models import Post


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    username = forms.CharField(min_length=4, max_length=35, validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]+$',
            message='Username isn\'t valid',
            code='invalid_username'
        )
    ])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


# class RegistrationForm(forms.ModelForm):
#     password = forms.CharField(label='Enter password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name')
#
#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password'] == cd['password2']:
#             return cd['password2']
#         else:
#             return forms.ValidationError('Password don\'t match')


class SettingForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'name', 'surname', 'description')


class PostAddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image', 'description',)

    def clean_image(self):
        image = self.image
        valid_extension = ['jpg', 'jpeg', 'png']
        extension = image.split('.')[-1].lower()
        if extension not in valid_extension:
            raise forms.ValidationError('Your image isn\'t valid')
        return image
