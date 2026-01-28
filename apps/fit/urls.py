from django.urls import path
from . import views

urlpatterns = [
    path('',views.logins,name="logins"),
    path("logout/", views.sesionout, name="logout"),
    path("register/", views.register_user, name="register")
]
