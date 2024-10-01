# accounts/forms.py
from django import forms
from django.contrib.auth.models import User

class ProfileUpdateForm(forms.ModelForm):
    # Additional fields not present in the default User model
    secondary_email = forms.EmailField(required=False, label="Secondary Email")
    phone_number = forms.CharField(required=False, label="Phone Number")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'secondary_email', 'phone_number', 'password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),  # Show current password in password field
        }
