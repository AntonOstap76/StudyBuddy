from django.urls import path
from . import views

# set a url patterns

urlpatterns=[
# home page is a root domain
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
]