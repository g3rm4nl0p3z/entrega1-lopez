from django.urls import path
from post.views import ver_posts, buscar_posts
from post.views import VerPostView, NuevoPostView, EditarPostView, EliminarPostView

urlpatterns = [
    path('', ver_posts, name='ver_posts'),
    path('buscar/', buscar_posts, name='buscar_posts'),
    path('post/<int:pk>', VerPostView.as_view(), name='ver_post'),
    path('nuevo/', NuevoPostView.as_view(), name='nuevo_post'),
    path('post/<int:pk>/editar/', EditarPostView.as_view(), name='editar_post'),
    path('post/<int:pk>/eliminar/', EliminarPostView.as_view(), name='borrar_post'),
]
