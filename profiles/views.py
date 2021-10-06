from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView
from accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserUpdateForm
from notes.models import Note
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    notes = Note.objects.filter(author=user)
    total_friends = 0
    total_followers = len(User.objects.filter(friends__contains=[user]))

    if user.friends:
        total_friends = len(user.friends)

    page = request.GET.get('page', 1)
    paginator = Paginator(notes, 20)
    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        notes = paginator.page(page)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)

    context = {
        'user_profile': user,
        'notes': notes,
        'total_friends': total_friends,
        'total_followers': total_followers,

    }

    return render(request, 'profiles/user_profile.html', context)


def user_following_list(request, pk):
    main_user = get_object_or_404(User, pk=pk)
    users_following = []
    results = []
    if main_user.friends:
        users_following = list(main_user.friends)

        for user_following in users_following:
            user = User.objects.get(username=user_following)
            results.append(user)
    return render(request, 'profiles/following_list.html', {'users_following': results})


def followers_list(request, pk):
    main_user = get_object_or_404(User, pk=pk)
    followers_query = User.objects.filter(friends__contains=[main_user])

    return render(request, 'profiles/followers_list.html', {'followers': followers_query, 'followed_user': main_user})


class UpdateUserView(UpdateView, LoginRequiredMixin):
    login_url = '/login/'
    model = User
    template_name = 'profiles/user_form.html'
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        return self.request.user
