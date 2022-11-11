from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import FormularioRegistro, FormularioEditarPerfil, FormularioCambiarPassword
from accounts.models import UserExtension
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required


def iniciar_sesion(request):

# Sólo permite el ingreso si NO se está logueado. Caso contrario, redirige a 'home'
# Esta validación es útil cuando se intenta ingresar forzando la URL
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        formulario_login = AuthenticationForm(request, data=request.POST)
        if formulario_login.is_valid():
            user = formulario_login.get_user()
            login(request, user)
            user_extension, es_nuevo_userextension = UserExtension.objects.get_or_create(user=request.user)
            return redirect('home')
    else:
        formulario_login = AuthenticationForm()

    return render(request, 'accounts/login.html', { 'formulario_login':formulario_login })


def registrar_cuenta(request):

# Sólo permite el ingreso si NO se está logueado. Caso contrario, redirige a 'home'
# Esta validación es útil cuando se intenta ingresar forzando la URL
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        formulario_registro = FormularioRegistro(request.POST)
        if formulario_registro.is_valid():
            formulario_registro.save()
            return redirect('home')
    else:
        formulario_registro = FormularioRegistro()

    return render(request, 'accounts/registrar.html', { 'formulario_registro':formulario_registro })


@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('home')


@login_required
def ver_perfil(request):
    return render(request, 'accounts/perfil.html')


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        formulario_editar_perfil = FormularioEditarPerfil(request.POST, request.FILES)

        if formulario_editar_perfil.is_valid():
            datos_perfil = formulario_editar_perfil.cleaned_data

            request.user.email = datos_perfil['email']
            request.user.first_name = datos_perfil['first_name']
            request.user.last_name = datos_perfil['last_name']

# En caso de blanquearse el avatar, el mismo se guardará vacío.
# En caso de cambiarlo, este será actualizado. De lo contrario, se mantendrá la imagen anterior
            if datos_perfil['avatar'] == False:
                request.user.userextension.avatar = None
            elif datos_perfil['avatar'] != None:
                request.user.userextension.avatar = datos_perfil['avatar']

            request.user.userextension.descripcion = datos_perfil['descripcion']
            request.user.userextension.link = datos_perfil['link']

            request.user.save()
            request.user.userextension.save()

            return redirect('ver_perfil')
    else:
        formulario_editar_perfil = FormularioEditarPerfil(
            initial={
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'avatar': request.user.userextension.avatar,
                'descripcion': request.user.userextension.descripcion,
                'link': request.user.userextension.link,
            }
        )

    return render(request, 'accounts/editar_perfil.html', { 'formulario_editar_perfil':formulario_editar_perfil })


@login_required
def cambiar_password(request):
    if request.method == 'POST':
        formulario_cambio_password = FormularioCambiarPassword(user=request.user, data=request.POST)

        if formulario_cambio_password.is_valid():
            formulario_cambio_password.save()
            update_session_auth_hash(request, request.user)
            return redirect('ver_perfil')
    else:
        formulario_cambio_password = FormularioCambiarPassword(user=request.user)

    return render(request, 'accounts/cambiar_password.html', { 'formulario_cambio_password':formulario_cambio_password })
