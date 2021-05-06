from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView
from accounts.models import User


# Create your views here.
def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    context = {
        'user': user
    }

    return render(request, 'profiles/user_profile.html', context)