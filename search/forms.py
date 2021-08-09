from django import forms


class FriendSearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class': 'searchInput',
                                                          'autocomplete': 'off',
                                                          'placeholder': 'Search for friends'}), label='')


class NoteSearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class': 'searchInput',
                                                          'autocomplete': 'off',
                                                          'placeholder': 'Search for notes'}), label='')