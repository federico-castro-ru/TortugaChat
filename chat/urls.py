from django.urls import path
from . import views

print("Running urls...")

app_name = 'chat'
urlpatterns = [
    path('', views.main_page, name='main_page'),
]