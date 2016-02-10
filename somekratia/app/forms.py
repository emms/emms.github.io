from django.forms import ModelForm, PasswordInput, CharField
from app.models import UserWithProfile
from django.contrib.auth.models import User


class UserForm(ModelForm):
    password = CharField(widget=PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(ModelForm):
    class Meta:
        model = UserWithProfile
        fields = ('picture',)

