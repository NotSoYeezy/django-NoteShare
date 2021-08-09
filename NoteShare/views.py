from django.views.generic import TemplateView
from django.shortcuts import render
from accounts.models import User
from notes.models import Note
from random import shuffle
import random


def index_view(request):
    friends = []

    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        friends_usernames = user.friends
        for username in friends_usernames:
            friends.append(User.objects.get(username=username))
    friends = random.sample(friends, len(friends))
    return render(request, 'index.html', {'friends': friends, 'notes': Note})


class InfoView(TemplateView):
    template_name = 'information_page.html'
