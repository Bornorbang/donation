from django import forms
from django.contrib.auth.models import User
from app.models import Donate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class SignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['full_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donate
        fields = ['full_name', 'email', 'phone', 'address', 'amount']

    def __init__(self, *args, **kwargs):
        super(DonationForm, self).__init__(*args, **kwargs)

        self.fields['full_name'].widget.attrs.update({'class': 'form-control', 'style': 'height: 50px;'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'style': 'height: 50px;'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'style': 'height: 50px;'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'style': 'height: 50px;'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Amount in $', 'style': 'height: 50px;'})
