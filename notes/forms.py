from django import forms
from .models import Note, Rate
from .validators import check_file_size


class NoteCreateForm(forms.ModelForm):
    # category = forms.ChoiceField(widget=forms.Select(attrs={'class': 'noteInput', 'id': 'cat_choice'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'noteInput'}))
    content_file = forms.FileField(widget=forms.FileInput(attrs={'id': 'file_field'}), required=False,
                                   validators=[check_file_size])
    description = forms.CharField(widget=forms.Textarea(attrs={'id': 'note_text'}), required=False,)
    thumbnail = forms.ImageField(validators=[check_file_size])

    class Meta:
        model = Note
        fields = ('category', 'title', 'content_file', 'description', 'thumbnail')


class RateForm(forms.ModelForm):

    class Meta:
        model = Rate
        fields = ('rate',)
