from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Note
from .forms import NoteCreateForm
from django.contrib.auth.decorators import login_required

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


class NoteDetailView(DetailView):
    model = Note
    template_name = 'notes/note_detail.html'


@login_required()
def note_delete_view(request, slug):
    note = get_object_or_404(Note, slug=slug)
    author_pk = note.author.pk

    if request.method == 'POST':
        if note.author == request.user:
            note.delete()
            print(author_pk)
            return redirect('profile', pk=author_pk)
        else:
            return redirect('profile', pk=author_pk)
    else:
        return redirect('notes:detail_note', slug=slug)


