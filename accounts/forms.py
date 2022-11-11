from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms


'''
    FORMULARIO FormularioRegistro:
    - Username: str
    - Email: str
    - Password1: str
    - Password2: str
'''
class FormularioRegistro(UserCreationForm):

    email     = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:'' for k in fields}


'''
    FORMULARIO FormularioEditarPerfil:
    - Email: str
    - First_name: str
    - Last_name: str
    - Descripcion: str
    - Link: str
    - Avatar: file
'''
class FormularioEditarPerfil(forms.Form):

    email       = forms.EmailField(required=True)
    first_name  = forms.CharField(label='Nombre', required=False)
    last_name   = forms.CharField(label='Apellido', required=False)
    avatar      = forms.ImageField(required=False, widget=forms.ClearableFileInput)
    descripcion = forms.CharField(max_length=255, required=False, widget=forms.Textarea)
    link        = forms.URLField(max_length=100, required=False)


'''
    FORMULARIO FormularioCambiarPassword:
    - Old_password: str
    - New_password1: str
    - New_password2: str
'''
class FormularioCambiarPassword(PasswordChangeForm):

    old_password  = forms.CharField(label='Password actual', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='Password nuevo', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirmar password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        help_texts = {k:'' for k in fields}
