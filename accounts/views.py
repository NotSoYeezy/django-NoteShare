from django.urls import reverse_lazy
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from django.contrib.auth import update_session_auth_hash
from .forms import UserChangePassword
from django.contrib.auth.decorators import login_required
from .models import User

app_name = 'accounts'


class LoginView(View):

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy('index'))
            else:
                return render(request, 'accounts/login.html', {'error_tag': 'User is not active'})
        else:
            return render(request, 'accounts/login.html', {'error_tag': 'Wrong credentials, try again'})

    def get(self, request):
        return render(request, 'accounts/login.html')


class LogoutView(View, LoginRequiredMixin):
    login_url = '/accounts/login/'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('index'))


def user_register(request):
    user_form = forms.UserSignupForm
    registered = False

    if request.method == 'POST':
        user_form = user_form(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)

    return render(request, 'accounts/register.html', {'user_form': user_form, 'registered': registered})


@login_required()
def change_password(request):
    if request.method == 'POST':
        form = UserChangePassword(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect(reverse('profile', kwargs={'pk': request.user.pk}))
        else:
            print(form.errors)
    else:
        form = UserChangePassword(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})


@login_required()
def delete_account(request):
    user = get_object_or_404(User, pk=request.user.pk)
    followers = User.objects.filter(friends__contains=[user.username])
    error = ''

    if request.method == 'POST':
        choice = request.POST['rdo']
        if str(choice) == 'Yes':
            if followers:
                # Removing followers, prevents index page from query error
                for follower in followers:
                    follower.friends.remove(user.username)
                    follower.save()
            user.delete()
            return redirect('index')
        elif str(choice) == 'No':
            return redirect('profile', pk=request.user.pk)
        else:
            error = 'There was an error, please try again'

    return render(request, 'accounts/confirm_delete.html', {'error': error})
