from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.urls import resolve, reverse_lazy
from django.http import HttpResponseRedirect


@login_required()
# Create your views here.
def add_friend(request, pk):
    friend = get_object_or_404(User, pk=pk)
    friend_adder = get_object_or_404(User, pk=request.user.pk)

    if friend_adder.friends:
        if friend.username not in friend_adder.friends:
            friend_adder.friends.append(friend.username)
            friend_adder.save()
        else:
            print('You are already friends!')
    else:
        friend_adder.friends = [friend.username]
        friend_adder.save()

    return redirect('profile', pk=friend.pk)


@login_required()
def remove_friend(request, pk):
    friend = get_object_or_404(User, pk=pk)
    friend_remover = get_object_or_404(User, pk=request.user.pk)

    if friend.username in friend_remover.friends:
        friend_remover.friends.remove(friend.username)
        friend_remover.save()

    return redirect('profile', pk=friend_remover.pk)
