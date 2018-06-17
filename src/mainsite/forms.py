from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label=_("Your email address"))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email", "avatar")


class UserSettingsForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ("username", "avatar")
