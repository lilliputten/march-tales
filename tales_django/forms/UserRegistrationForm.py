from django import forms
from django.contrib.auth import get_user_model
from django_registration.forms import RegistrationForm as BaseRegistrationForm


class UserRegistrationForm(BaseRegistrationForm):

    # @see https://django-registration.readthedocs.io/en/3.4/custom-user.html

    # NOTE: Don't display address?
    # address = forms.CharField(
    #     required=False,
    #     widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}),
    # )

    class Meta:
        model = get_user_model()
        fields = [
            #  'username',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
            # "address",
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            #  'username' : forms.HiddenInput(),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["first_name"].required = True
        # self.fields["last_name"].required = True
