from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.shortcuts import redirect, render

from core.helpers.dates import this_year

from ..forms import MembershipForm
from ..models import Membership


def membership_application(request: HttpRequest):
    if not request.user:
        messages.error(
            request,
            'You have to have an account before you can register for membership',
        )
        return redirect('login')
    if not request.user.is_authenticated:
        messages.error(
            request,
            'You have to authenticate your account before you can register for membership',
        )
        return redirect('login')

    try:
        membership = Membership.objects.get(user=request.user)
        if membership.active:
            messages.error(request, f'You are already a {settings.SITE_SHORT_NAME} member')
            return redirect('profile')
    except ObjectDoesNotExist:
        pass

    if request.method == 'POST':
        form = MembershipForm(request.POST)

        if form.is_valid():
            pass
            # TODO: Create a payment!
            # payment = Payment(
            #     status="CREATED",
            #     data={
            #         "user": {
            #             "id": request.user.id,
            #             "name": form.cleaned_data["name"],
            #             "address": form.cleaned_data["address"],
            #         },
            #         "extra": form.cleaned_data["extra"],
            #         "kind": "membership",
            #         "membership": {
            #             "type": form.cleaned_data["membership_type"],
            #             "label": MEMBERSHIP_DATA[form.cleaned_data["membership_type"]][
            #                 "label"
            #             ],
            #         },
            #         "method": form.cleaned_data["payment_method"],
            #         "price": MEMBERSHIP_DATA[form.cleaned_data["membership_type"]][
            #             "price"
            #         ],
            #         "currency": MEMBERSHIP_DATA[form.cleaned_data["membership_type"]][
            #             "currency"
            #         ],
            #         "until": this_year(),
            #     },
            # )
            # payment.save()

            try:
                membership = Membership.objects.get(user=request.user)
                membership.mailing_list = form.cleaned_data['mailing_list']
                membership.membership_type = form.cleaned_data['membership_type']
                membership.until = this_year()
                # membership.payment = payment # TODO!
                membership.save()
            except ObjectDoesNotExist:
                membership = Membership(
                    user=request.user,
                    membership_type=form.cleaned_data['membership_type'],
                    # payment=payment, # TODO!
                    mailing_list=form.cleaned_data['mailing_list'],
                )
                membership.save()

            # # TODO: Update payment data
            # if payment.data["method"] == "INVOICE":
            #     payment.status = "ISSUED"
            #     payment.save()
            #     payment.email_invoice()
            #     messages.success(
            #         request,
            #         f"Your membership has been created! An invoice has been sent to {request.user.email} from {settings.CONTACT_EMAIL}. The invoice can also be downloaded from your profile. Please note your membership is not in force until the invoice is paid.",
            #     )
            #     return redirect("profile")
            # elif payment.data["method"] == "STRIPE":
            #     return redirect("payment_stripe", payment_id=payment.id)
    else:
        form = MembershipForm(
            initial={
                'name': request.user.get_full_name(),
                'address': request.user.address,
                'extra': '',
            }
        )

    return render(
        request=request,
        template_name='tales_django/membership/membership_start.html.django',
        context={'form': form},
    )
