from django.shortcuts import render
from accounts.models import User
from notes.models import Note
from django.contrib.postgres.search import SearchVector, TrigramSimilarity
from .forms import FriendSearchForm, NoteSearchForm


# Create your views here.
def user_search_view(request):
    search_form = FriendSearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        search_form = FriendSearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            results = User.objects.annotate(similarity=TrigramSimilarity('display_name', query),)\
                .filter(similarity__gt=0.1).order_by('-similarity')

    return render(request, 'search/friend_search.html', {'form': search_form, 'query': query, 'results': results})


def note_search_view(request):
    search_form = NoteSearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        search_form = NoteSearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            results = Note.objects.annotate(similarity=TrigramSimilarity('title', query),)\
                .filter(similarity__gt=0.1).order_by('-similarity')

    return render(request, 'search/note_search.html', {'form': search_form, 'query': query, 'results': results})
