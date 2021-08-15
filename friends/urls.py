from django.urls import path
from . import views

app_name = 'friends'

urlpatterns = [
    path('add_friend/<str:pk>', views.add_friend, name='add_friend'),
    path('remove_friend/<str:pk>', views.remove_friend, name='remove_friend'),
]