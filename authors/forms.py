from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your password',
        }),
        label='Password',
        error_messages={
            'required': 'Password must not be empty',
        }
    )
    password_2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
        }),
        label='Confirm Password',
        error_messages={
            'required': 'Password must not be empty',
        }
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        # exclude = [...]

        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
        }

        help_texts = {
            'email': 'The email must be valid',
        }

        error_messages = {
            'required': 'This field must not be empty',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Ex.: John',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Ex.: Ohen',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Ex.: email@email.com',
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'Your Username',
            }),
        }
