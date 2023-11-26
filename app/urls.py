from django.urls import path
from . import views
#from .views import HomePageView, AboutPageView
from django.conf import settings

urlpatterns = [
    path('', views.app_home, name='app_home'),
    path('persona/create/', views.create_persona, name='create_persona'),
    path('persona/delete/<int:persona_id>/', views.delete_persona, name='delete_persona'),
    path('chat/<int:persona_id>/', views.persona_detail, name='persona_detail'),
    path('persona/<int:persona_id>/', views.persona_profile, name='persona_profile'),

]
