# @module tales_django/views/registration.py
# @changed 2024.12.31, 13:13

from django_registration.backends.activation.views import (
    RegistrationView as BackendRegistrationView,
)

from ..forms import UserRegistrationForm


class UserRegistrationView(BackendRegistrationView):
    form_class = UserRegistrationForm

    def get_form_class(self):
        """Return the form class to use."""
        return self.form_class

    def get_form(self, form_class=None):
        form_class = UserRegistrationForm
        return form_class(**self.get_form_kwargs())
