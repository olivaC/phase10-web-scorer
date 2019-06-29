from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django import forms

from phase10Scorer.settings import PASSWORD


class LoginForm(forms.Form):
    """
    Form used to log in to the web application.
    """
    username = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=128)), label="Username")

    class Meta:
        fields = ['username', ]

    def clean(self):
        try:
            User.objects.get(username__iexact=self.cleaned_data['username'])
            user = authenticate(username=self.cleaned_data['username'], password=PASSWORD)
            if user is not None:
                if not user.is_authenticated:
                    raise forms.ValidationError("Username/password not found.")
            else:
                raise forms.ValidationError("Username not found.")
        except User.DoesNotExist:
            raise forms.ValidationError("Username doesn't exist")
        return self.cleaned_data


class UserCreateForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=128)), label="Username")

    class Meta:
        model = User
        fields = ('username',)

    def clean(self):
        try:
            User.objects.get(username__iexact=self.cleaned_data['username'])
            raise forms.ValidationError('Username already exists.')
        except:
            return self.cleaned_data
