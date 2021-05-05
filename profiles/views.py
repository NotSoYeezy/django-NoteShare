from django.shortcuts import render, get_object_or_404
from accounts.models import User


# Create your views here.
def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    context = {
        'user': user
    }

    return render()