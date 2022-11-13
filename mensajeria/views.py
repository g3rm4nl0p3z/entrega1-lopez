from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import DeleteView

from mensajeria.models import Chat, Mensaje
from mensajeria.forms import FormularioIniciarConversacion, FormularioEnvioMensaje

'''
    VISTAS BASADAS EN FUNCIONES:
    -    Ver chats: Muestro TODAS las conversaciones iniciadas con usuarios
    -     Ver chat: Muestro la conversacion iniciada con un usuario
    - Iniciar chat: Inicia una nueva conversacion con el usuario seleccionado
'''
@login_required
def ver_chats(request):
# Búsqueda de TODAS las conversaciones recibidas e iniciadas por el usuario
    chats = Chat.objects.all().filter(user_chat_2=request.user).union(
            Chat.objects.all().filter(user_chat_1=request.user)
    ).order_by('id')

    return render(request, 'mensajeria/ver_chats.html', { 'chats' : chats })


@login_required
def iniciar_chat(request):

# Esta vista permite el inicio de una nueva conversación con el usuario seleccionado
    if request.method == 'POST':
        formulario_iniciar_chat = FormularioIniciarConversacion(request.POST)

        chat_user = formulario_iniciar_chat.data.get('user_chat_2')

        nuevo_chat = Chat(
            user_chat_1 = request.user,
            user_chat_2 = User.objects.get(username=chat_user)
        )

        nuevo_chat.save()

        return redirect('ver_chat', nuevo_chat.id)
    else:
# Búsqueda de TODAS las conversaciones recibidas e iniciadas por el usuario
# Obtengo un QuerySet más pequeño, con los usuarios con chats activos
        try:
            qs_chats = Chat.objects.all().filter(user_chat_2=request.user).values_list('user_chat_1', flat=True).union(
                        Chat.objects.all().filter(user_chat_1=request.user).values_list('user_chat_2', flat=True)
            )

# Filtro usuarios 'staff' y con chats activos
# Disponibiliza SÓLO aquellos usuarios con los que puedo iniciar una conversación
            qs_users = User.objects.all().filter(is_staff=False).exclude(username=request.user.username).exclude(pk__in=qs_chats)

            qs_users = qs_users.order_by('username')
        except:
            qs_users = User.objects.none()

        formulario_iniciar_chat = FormularioIniciarConversacion()

        formulario_iniciar_chat.fields['user_chat_2'].queryset = qs_users

    return render(request, 'mensajeria/iniciar_conversacion.html', { 'formulario_iniciar_chat' : formulario_iniciar_chat })


@login_required
def ver_chat(request, id):

# Búsqueda de los datos de la conversación
    chat = Chat.objects.get(id=id)

    mensajes = None

# Esta vista disponibiliza la conversación con el usuario, y permite enviar un nuevo mensaje
    if request.method == 'POST':
        formulario_envio_mensaje = FormularioEnvioMensaje(request.POST)

        if formulario_envio_mensaje.is_valid():
            datos_mensaje = formulario_envio_mensaje.cleaned_data

            nuevo_mensaje = Mensaje(
                chat = chat,
                de_user = request.user,
                contenido = datos_mensaje['contenido']
            )

            nuevo_mensaje.save()
            return redirect('ver_chat', chat.id)
    else:
        mensajes = Mensaje.objects.filter(chat=chat).order_by('id')

        formulario_envio_mensaje = FormularioEnvioMensaje()

    return render(request, 'mensajeria/ver_chat.html', { 'formulario_envio_mensaje' : formulario_envio_mensaje, 'chat' : chat, 'mensajes' : mensajes })

'''
    CLASES BASADAS EN VISTAS (CBV):
    - Borrar: EliminarChatView
'''
class EliminarChatView(LoginRequiredMixin, DeleteView):
    model         = Chat
    template_name = 'mensajeria/borrar_chat.html'
    success_url   = '/chats/'
