"""NoteShare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from profiles import views as profile_views

urlpatterns = [
    # MAIN VIEWS
    path('admin/', admin.site.urls),
    path('', views.Index.as_view(), name='index'),
    path('Informations/', views.InfoView.as_view(), name='information'),
    path('user/<str:pk>/', profile_views.user_profile, name='profile'),
    path('user/<str:pk>/update/', profile_views.UpdateUserView.as_view(), name='profile_update'),

    # OTHER APPS' VIEWS
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('accounts.urls')),
    path('Notes/', include('notes.urls')),
    path('search/', include('search.urls')),
    path('friends/', include('friends.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
