from django import forms
from accounts.models import User


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'loginInput'}), label='Change username')
    bio = forms.CharField(widget=forms.Textarea(attrs={'id': 'bioText'}), label='Change bio')
    profile_pic = forms.ImageField(widget=forms.FileInput(), label='Update profile pic')

    class Meta:
        model = User
        fields = ('username', 'bio', 'profile_pic', )
