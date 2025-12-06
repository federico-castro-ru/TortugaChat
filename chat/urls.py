from django.urls import path
from . import views

print("Running urls...")

app_name = 'chat'
urlpatterns = [
    path('', views.index, name='main_page'),
]