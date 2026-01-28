from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('mispesos/', views.mispesos, name="mispesos"),
    path('editpeso/<int:id_peso>',views.editpeso,name='editpeso'),
    path("createpeso/", views.createpeso, name="createpeso"),
    path("objetivos/", views.conobjetivos, name="objetivos")
]
