from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from .models import User
from datetime import date



def year_set(year):
    year_list = list()
    for i in range(year, date.today().year + 1):
        year_list.append(i)
    return year_list

YEAR_CHOICE = year_set(1900)

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)
    town = forms.CharField(required=False, max_length=100)
    birth_date = forms.DateField(required=False, widget=forms.SelectDateWidget(years=YEAR_CHOICE))
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'town', 'birth_date',
                'password1', 'password2')
        

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.town = self.cleaned_data['town']
        user.birth_date = self.cleaned_data['birth_date']
        if commit:
            user.save()
        return user

class CustomAuthencticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        "autofocus": True,
        'class' : 'ui input'
        }))
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            'class' : 'ui input'
            }),
    )

class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    town = forms.CharField(required=False, max_length=100)
    birth_date = forms.DateField(required=False, widget=forms.SelectDateWidget(years=YEAR_CHOICE))
    initial_fields = ['first_name', 'last_name', 'town', 'birth_date']

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'town', 'birth_date']
    
