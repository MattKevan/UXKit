from django.urls import path
from . import views
#from .views import HomePageView, AboutPageView
from django.conf import settings

urlpatterns = [
    path('', views.app_home, name='app_home'),
    path('create/', views.create_persona, name='create_persona'),
    path('<uuid:persona_hash>/delete/', views.delete_persona, name='delete_persona'),
    path('<uuid:persona_hash>/', views.persona_detail, name='persona_detail'),
    path('<uuid:persona_hash>/view/', views.persona_profile, name='persona_profile'),
    path('<uuid:persona_hash>/edit/', views.edit_persona, name='edit_persona'),

]
