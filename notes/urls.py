from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('create/', views.NoteCreateView.as_view(), name='create_note'),
    path('note/<str:slug>', views.note_detail_view, name='detail_note'),
    path('note/<str:slug>/delete', views.note_delete_view, name='delete_note')
]