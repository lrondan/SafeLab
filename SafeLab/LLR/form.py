from django import forms
from .models import Register_User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register_User
        fields = [
            'username',
            'email',
            'password',
            'confirm_password',
            'date',
            ]