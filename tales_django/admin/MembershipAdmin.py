import zipfile
from io import BytesIO

from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Q
from django.http import HttpResponse

from ..models import (
    Membership,
    # User,
    # Event,
    # Message,
    # Payment,
    # Registration,
    # RegistrationOption,
)


class MembershipAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'started',
        'until',
        #  "paid",
        'active',
        'membership_type',
    ]


admin.site.register(Membership, MembershipAdmin)
