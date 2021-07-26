from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class': 'searchInput',
                                                          'autocomplete': 'off',
                                                          'placeholder': 'Search for friends'}), label='')
