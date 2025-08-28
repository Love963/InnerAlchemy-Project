from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Your email'}),
        help_text="Required. Enter a valid email address."
    )
    avatar = forms.ImageField(required=False)
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself'})
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'bio', 'avatar', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username


class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Update your bio'})
    )
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'bio', 'avatar']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        qs = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This username is already taken.")
        return username
