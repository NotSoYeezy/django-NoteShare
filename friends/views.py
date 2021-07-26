from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.urls import resolve, reverse_lazy
from django.http import HttpResponseRedirect


@login_required()
# Create your views here.
def add_friend(request, pk, query):
    friend = get_object_or_404(User, pk=pk)
    friend_adder = get_object_or_404(User, pk=request.user.pk)

    if friend.username not in friend_adder.friends:
        friend_adder.friends.append(friend.username)
        friend_adder.save()
    else:
        print('You are already friends!')

    return HttpResponseRedirect(reverse_lazy('search:user_search'))


