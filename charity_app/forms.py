from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Donation
from django.contrib.auth import authenticate

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'surname', 'password1', 'password2', )


class CustomUserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class AddDonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = '__all__'
