__author__ = 'rajatgoyal'

# Imports
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):

    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        """ Do the login validation here."""

        clean = super(LoginForm, self).clean()
        username = clean.get("username")
        password = clean.get("password")

        if (username and password):
            if User.objects.filter(username=username).exists():
                user = authenticate(username=username, password=password)
                if not(user and user.is_active):
                    self._errors['username'] = self.error_class([
                            "Username and Password you enterd do not match"])
                    raise forms.ValidationError("")

            else:
                self._errors['username'] = self.error_class([
                        "That username does not exist in our database"])
                raise forms.ValidationError("")

        return clean