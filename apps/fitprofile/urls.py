from django.urls import path
from . import views
urlpatterns = [
    path('',views.fitprofiles,name='fitprofiles')    
]
