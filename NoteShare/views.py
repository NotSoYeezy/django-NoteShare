from django.views.generic import TemplateView
from django.shortcuts import render
from accounts.models import User
from notes.models import Note
from el_pagination.views import AjaxListView
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index_view(request):
    friends = []

    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        if user.friends:
            friends_usernames = user.friends
            for username in friends_usernames:
                friends.append(User.objects.get(username=username))
            friends = random.sample(friends, len(friends))
    page = request.GET.get('page', 1)
    paginator = Paginator(friends, 2)
    try:
        friends = paginator.page(page)
    except PageNotAnInteger:
        friends = paginator.page(page)
    except EmptyPage:
        friends = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'friends': friends, 'notes': Note})


class InfoView(TemplateView):
    template_name = 'information_page.html'
