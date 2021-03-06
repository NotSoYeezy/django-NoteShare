from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('users/', views.user_search_view, name='user_search'),
    path('notes/', views.note_search_view, name='note_search')
]
