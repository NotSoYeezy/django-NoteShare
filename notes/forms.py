from django import forms
from .models import Note, Rate
from .validators import check_file_extension
from NoteShare.settings import MEDIA_ROOT


class NoteCreateForm(forms.ModelForm):
    # category = forms.ChoiceField(widget=forms.Select(attrs={'class': 'noteInput', 'id': 'cat_choice'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'noteInput'}))
    content_file = forms.FileField(widget=forms.FileInput(attrs={'id': 'file_field'}), required=False)
    content_text = forms.CharField(widget=forms.Textarea(attrs={'id': 'note_text'}), required=False)

    def save(self, *args, **kwargs):
        cleaned_data = super(NoteCreateForm, self).clean()
        content_file = cleaned_data.get('content_file')
        super().save(*args, **kwargs)

    class Meta:
        model = Note
        fields = ('category', 'title', 'content_file', 'content_text', 'thumbnail')


class RateForm(forms.ModelForm):

    class Meta:
        model = Rate
        fields = ('rate',)
