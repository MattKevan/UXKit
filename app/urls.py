from django.urls import path
from . import views
#from .views import HomePageView, AboutPageView
from django.conf import settings

urlpatterns = [
    # Dashboard
    path('', views.app_home, name='app_home'),
    
    # Projects
    path('projects/', views.projects, name='projects'),
    path('projects/create/', views.project_create, name='project_create'),
    path('<uuid:project_hash>/', views.project_read, name='project_read'),
    path('<uuid:project_hash>/delete/', views.project_delete, name='project_delete'),

    # Lean UX canvases
    path('<uuid:project_hash>/ux-canvas/create/', views.lean_ux_canvas_create, name='lean_ux_canvas_create'),
    path('ux-canvas/<uuid:lean_ux_canvas_hash>/', views.lean_ux_canvas_read, name='lean_ux_canvas_read'),
    path('ux-canvas/<uuid:lean_ux_canvas_hash>/delete/', views.lean_ux_canvas_delete, name='lean_ux_canvas_delete'),
    
    # Personas 
    path('persona/create/', views.create_persona, name='create_persona'),
    path('persona/<uuid:persona_hash>/', views.persona_detail, name='persona_detail'),
    path('persona/<uuid:persona_hash>/profile/', views.persona_profile, name='persona_profile'),
    path('persona/<uuid:persona_hash>/edit/', views.edit_persona, name='edit_persona'),
    path('persona/uuid:persona_hash>/delete/', views.delete_persona, name='delete_persona'),
    
]
