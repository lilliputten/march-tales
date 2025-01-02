from django.contrib import admin

from ..models import (
    Membership,
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
