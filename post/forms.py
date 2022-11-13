from django import forms

'''
    FORMULARIO FormularioBuscarPosts:
    - Titulo: str
'''
class FormularioBuscarPosts(forms.Form):
    titulo = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={ 'class' : 'form-control' }))
