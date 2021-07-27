from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView
from accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserUpdateForm
from notes.models import Note
from django.contrib.postgres.search import SearchVector


# Create your views here.
def user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    notes = Note.objects.filter(author=user)
    total_friends = 0

    if user.friends:
        total_friends = len(user.friends)

    context = {
        'user_profile': user,
        'notes': notes,
        'total_friends': total_friends,

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


class UpdateUserView(UpdateView, LoginRequiredMixin):
    login_url = '/login/'
    model = User
    template_name = 'profiles/user_form.html'
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        return self.request.user
