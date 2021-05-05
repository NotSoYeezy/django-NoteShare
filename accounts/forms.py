from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSignupForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'loginInput'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'loginInput'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'loginInput'}), validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'loginInput'}))
    profile_pic = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'profile_pic')

    field_order = ['username', 'email', 'password', 'confirm_password', 'profile_pic']

#   Cleaning data to get password input and check if passwords match
    def clean(self):
        cleaned_data = super(UserSignupForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match"
            )