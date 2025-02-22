from django import forms
from .models import Register_User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register_User
        fields = [
            'username',
            'email',
            'password',
            ]
        
    def clean_email(self):
        email_passed = self.cleaned_data.get('email')
        email_passed = email_passed.lower()
        email_already_registered = Register_User.objects.filter(email=email_passed).exists()
        if email_already_registered:
            raise forms.ValidationError('Email already registered')  
        elif  email_already_registered:
            Register_User.objects.filter(email=email_passed).delete()
        return email_passed  