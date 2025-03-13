from unfold.sites import UnfoldAdminSite

class NewUnfoldAdminSite(UnfoldAdminSite):
    pass

# You can route to new admin by "original-name-here-not-admin:index"
unfold_admin_site = NewUnfoldAdminSite(name='unfold-admin')
