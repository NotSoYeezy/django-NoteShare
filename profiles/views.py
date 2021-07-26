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
    friends = user.friends

    context = {
        'user_profile': user,
        'notes': notes,
        'friends': friends,

    }

    return render(request, 'profiles/user_profile.html', context)


class UpdateUserView(UpdateView, LoginRequiredMixin):
    login_url = '/login/'
    model = User
    template_name = 'profiles/user_form.html'
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        return self.request.user


