from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from post.models import Post
from post.forms import FormularioBuscarPosts

'''
    VISTAS BASADAS EN FUNCIONES:
    -    Ver posts: Muestro TODOS las paginas creadas por los usuarios
    - Buscar posts: Filtro paginas por titulo
'''
def ver_posts(request):
    posts = Post.objects.all().order_by('id')
    return render(request, 'post/ver_posts.html', { 'posts' : posts })


def buscar_posts(request):
    titulo = request.GET.get('titulo', None)

    if titulo:
        posts = Post.objects.filter(titulo__icontains=titulo)
    else:
        posts = Post.objects.all()

    posts = posts.order_by('id')

    formulario_buscar_posts = FormularioBuscarPosts()

    return render(request, 'post/buscar_posts.html', { 'formulario_buscar_posts' : formulario_buscar_posts, 'posts' : posts })

'''
    CLASES BASADAS EN VISTAS (CBV):
    -    Ver: VerPostView
    -  Crear: NuevoPostView
    - Editar: EditarPostView
    - Borrar: EliminarPostView
'''
class VerPostView(DetailView):
    model         = Post
    template_name = 'post/ver_post.html'


class NuevoPostView(LoginRequiredMixin, CreateView):
    model         = Post
    template_name = 'post/crear_post.html'
    success_url   = '/posts/'
    fields        = ['titulo', 'subtitulo', 'contenido', 'imagen']

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class EditarPostView(LoginRequiredMixin, UpdateView):
    model         = Post
    template_name = 'post/editar_post.html'
    success_url   = '/posts/'
    fields        = ['titulo', 'subtitulo', 'contenido', 'imagen']


class EliminarPostView(LoginRequiredMixin, DeleteView):
    model         = Post
    template_name = 'post/borrar_post.html'
    success_url   = '/posts/'
