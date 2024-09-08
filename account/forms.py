from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2','is_writer']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control w-100'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control w-100'}),
            'username': forms.TextInput(attrs={'class': 'form-control w-100'}),
            'email': forms.EmailInput(attrs={'class': 'form-control w-100'}),
        }
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Enlever le texte d'aide pour le champ 'username'
        self.fields['username'].help_text = ''

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


