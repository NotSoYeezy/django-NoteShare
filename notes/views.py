from django.shortcuts import render, HttpResponseRedirect, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Note
from .forms import NoteCreateForm


# Create your views here.
class NoteCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Note
    form_class = NoteCreateForm
    template_name = 'notes/create_note.html'

    def form_valid(self, form):
        success_url = HttpResponseRedirect(reverse_lazy('profile', kwargs={'pk': self.request.user.pk}))
        form.instance.author = self.request.user
        content_file = self.request.FILES['content_file']
        form.save()
        return success_url
