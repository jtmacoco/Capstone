from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username","email","password1","password2"]
class StocksForm(forms.Form):
    stock=forms.CharField(label='Stock',max_length=50)        