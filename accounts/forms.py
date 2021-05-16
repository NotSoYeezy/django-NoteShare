from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
User = get_user_model()


class UserSignupForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'loginInput'}))
    display_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'loginInput'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'loginInput'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'loginInput'}), validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'loginInput'}))
    profile_pic = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'profile_pic', 'display_name', )

    field_order = ['username', 'display_name', 'email', 'password', 'confirm_password', 'profile_pic']

#   Cleaning data to get password input and check if passwords match
    def clean(self):
        cleaned_data = super(UserSignupForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match"
            )


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='Enter email:', widget=forms.EmailInput(attrs={'class': 'loginInput'}))


class UserSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(UserSetPasswordForm, self).__init__(*args, **kwargs)

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'loginInput'}),
                               validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'loginInput'}))

    #   Cleaning data to get password input and check if passwords match
    def clean(self):
        cleaned_data = super(UserSetPasswordForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match"
            )


class UserChangePassword(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserChangePassword, self).__init__(*args, **kwargs)

    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput(attrs={'class': 'loginInput'}))
    new_password1 = forms.CharField(label='Old password', widget=forms.PasswordInput(attrs={'class': 'loginInput'}))
    new_password2 = forms.CharField(label='Old password', widget=forms.PasswordInput(attrs={'class': 'loginInput'}))