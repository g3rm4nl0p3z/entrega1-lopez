from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from home.views import home, about

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
