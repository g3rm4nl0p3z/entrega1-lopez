from django.urls import path
from accounts.views import iniciar_sesion, registrar_cuenta, cerrar_sesion, ver_perfil, editar_perfil, cambiar_password

urlpatterns = [
    path('login/', iniciar_sesion, name='login'),
    path('registro/', registrar_cuenta, name='registrar'),
    path('logout/', cerrar_sesion, name='logout'),
    path('perfil/', ver_perfil, name='ver_perfil'),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),
    path('perfil/cambiar-password/', cambiar_password, name='cambiar_password'),
]
