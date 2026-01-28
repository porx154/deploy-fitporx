from django.urls import path
from . import views
urlpatterns = [
    path('profile/',views.fitprofiles,name='fitprofiles')    
]
