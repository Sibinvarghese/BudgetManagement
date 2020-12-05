from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from Budget.models import Expenses



class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password1","password2"]

class LoginForm(forms.Form):
    username=forms.CharField(max_length=120)
    password=forms.CharField(max_length=120)
    def clean(self):
        print("inside clean validate user and password")


class ReviewExpense(forms.Form):
    user=forms.HiddenInput()
    from_date=forms.DateField(widget=forms.SelectDateWidget())
    to_date = forms.DateField(widget=forms.SelectDateWidget())


class AddExpensForm(ModelForm):
    user=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model=Expenses
        fields=["category","amount","note","user"]


