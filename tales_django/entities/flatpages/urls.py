from django.urls import path

# from django.contrib.flatpages import views
from . import views

urlpatterns = [
    path('<path:url>', views.flatpage, name='django.contrib.flatpages.views.flatpage'),
]
