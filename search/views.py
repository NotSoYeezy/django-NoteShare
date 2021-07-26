from django.shortcuts import render
from accounts.models import User
from django.contrib.postgres.search import SearchVector, TrigramSimilarity
from .forms import SearchForm


# Create your views here.
def user_search_view(request):
    search_form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            results = User.objects.annotate(similarity=TrigramSimilarity('display_name', query),)\
                .filter(similarity__gt=0.1).order_by('-similarity')

    return render(request, 'search/friend_search.html', {'form': search_form, 'query': query, 'results': results})

