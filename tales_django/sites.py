from unfold.sites import UnfoldAdminSite
from allauth.account.views import login

# from django.utils.translation import gettext_lazy as _


class NewUnfoldAdminSite(UnfoldAdminSite):
    def login(self, request, extra_context=None):
        # Use Allauth‘s login
        return login(request)


# You can route to new admin by "original-name-here-not-admin:index"
unfold_admin_site = NewUnfoldAdminSite(name='unfold-admin')
