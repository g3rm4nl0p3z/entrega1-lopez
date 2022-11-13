from django.urls import path
from home.views import home, about

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
]
