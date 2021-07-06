from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Note, Rate
from .forms import NoteCreateForm, RateForm
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

    def get_context_data(self, **kwargs):
        context = super(NoteDetailView, self).get_context_data(**kwargs)
        context['form'] = RateForm
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.note = Note.objects.get(slug=self.kwargs['slug'])
        form.save()


def note_detail_view(request, slug):
    note = get_object_or_404(Note, slug=slug)
    form = RateForm

    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            if not Rate.objects.all().filter(author=request.user, note=note):
                form.instance.author = request.user
                form.instance.note = note
                form.save()
                return render(request, 'notes/note_detail.html', {'note': note,
                                                                  'form': form,
                                                                  'user_rate': form.cleaned_data['rate']})
            else:
                user_rate = Rate.objects.get(author=request.user, note=note)
                new_rate = form.cleaned_data['rate']
                user_rate.rate = new_rate
                user_rate.save()
                return render(request, 'notes/note_detail.html', {'note': note,
                                                                  'form': form,
                                                                  'message': "You've changed your rate!",
                                                                  'user_rate': user_rate.rate})
    else:
        try:
            if Rate.objects.get(author=request.user, note=note).rate:
                user_rate = Rate.objects.get(author=request.user, note=note).rate
                return render(request, 'notes/note_detail.html', {'note': note, 'form': form, 'user_rate': user_rate})
        except Rate.DoesNotExist:
            pass
    return render(request, 'notes/note_detail.html', {'note': note, 'form': form, 'user_rate': 0})


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


