from django import forms
from django.contrib.auth import get_user_model


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    #  is_active = forms.CharField(widget=forms.HiddenInput(), required=False)  # ???

    # address = forms.CharField(
    #     required=False,
    #     widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
    # )

    class Meta:
        model = get_user_model()
        fields = [
            'email',  # Needs re-activation
            'first_name',
            'last_name',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["first_name"].required = True
        # self.fields["last_name"].required = True
