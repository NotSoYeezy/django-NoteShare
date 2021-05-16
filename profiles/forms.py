from django import forms
from accounts.models import User


class UserUpdateForm(forms.ModelForm):
    display_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'loginInput'}), label='Change display name')
    bio = forms.CharField(widget=forms.Textarea(attrs={'id': 'bioText'}), label='Change bio', required=False)
    profile_pic = forms.ImageField(widget=forms.FileInput(), label='Update profile pic', required=False)

    class Meta:
        model = User
        fields = ('display_name', 'bio', 'profile_pic', )
