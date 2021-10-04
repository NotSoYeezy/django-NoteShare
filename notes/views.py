from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Note, Rate
from .forms import NoteCreateForm, RateForm
from django.contrib.auth.decorators import login_required


# Create your views here.
class NoteCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    model = Note
    form_class = NoteCreateForm
    template_name = 'notes/create_note.html'

    def form_valid(self, form):
        success_url = HttpResponseRedirect(reverse_lazy('profile', kwargs={'pk': self.request.user.pk}))
        form.instance.author = self.request.user
        content_file = self.request.FILES['content_file']
        form.save()
        return success_url


def note_detail_view(request, slug):
    note = get_object_or_404(Note, slug=slug)
    form = RateForm

    if request.method == 'POST':
        if request.user.is_authenticated:
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
        if request.user.is_authenticated:
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
    error = ''

    if request.method == 'POST':
        choice = request.POST['rdo']
        if str(choice) == 'Yes':
            if note.author == request.user:
                note.delete()
                return redirect('profile', pk=author_pk)
            else:
                return redirect('profile', pk=author_pk)
        elif str(choice) == 'No':
            return redirect('notes:detail_note', slug=note.slug)
        else:
            error = 'There was an error, please try again'
            return render(request, 'notes/confirm_delete.html', {'error': error, 'note': note})
    else:
        return render(request, 'notes/confirm_delete.html', {'error': error, 'note': note})


