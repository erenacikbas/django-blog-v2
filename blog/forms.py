from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# New User Orm
class NewUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            field.widget.attrs['placeholder'] = field.label
            field.label = ''
        self.fields['email'].required = True

    # username = forms.CharField(widget=forms.TextInput(
    #     attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Username',
    #         'id': 'inputUsername'
    #     }))
    # email = forms.CharField(widget=forms.EmailInput(
    #     attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Email',
    #         'id': 'inputEmail',
    #         'help_text': 'helptext'
    #     }))
    # password1 = forms.CharField(widget=forms.PasswordInput(
    #     attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Password',
    #         'id': 'inputPassword',
    #     }))
    # password2 = forms.CharField(widget=forms.PasswordInput(
    #     attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Password (Again)',
    #         'id': 'inputPassword2',
    #     }))

    # email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    # def clean(self):
    #     cleaned_data = super(NewUserForm, self).clean()
    #     password = cleaned_data.get("password")
    #     confirm_password = cleaned_data.get("confirm_password")

    #     if password != confirm_password:
    #         raise forms.ValidationError(
    #             "password and confirm_password does not match"
    #         )

    # def save(self, commit=True):
    #     user = super(NewUserForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     user.password = self.cleaned_data['password']
    #     if commit:
    #         user.save()
    #     return user


# Login Form
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            field.widget.attrs['placeholder'] = field.label
            field.label = ''

    # username = forms.EmailField(widget=forms.TextInput(
    #     attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Username',
    #         'id': 'hello'
    #     }))
    # password = forms.CharField(widget=forms.PasswordInput(
    #     attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Password',
    #         'id': 'hi',
    #     }))
