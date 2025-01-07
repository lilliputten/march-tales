from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib import admin


class Group(DjangoGroup):
    """Instead of trying to get new user under existing `Aunthentication and Authorization`
    banner, create a proxy group model under our Accounts app label.
    Refer to: https://github.com/tmm/django-username-email/blob/master/cuser/admin.py
    """

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        proxy = True


admin.site.unregister(DjangoGroup)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass
