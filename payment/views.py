from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from app import render, is_post
from app.views import data_view
from app.auth import login_required, officials_only, complete_profile_required
from board.models import Board
from scholarship.models import Scholarship, Application
from .filters import PaymentFilter
from .payment import payment
from .models import Payment


# Create your views here.
@officials_only()
def index(request):
    filter = PaymentFilter(request.GET, queryset=Payment.objects.all())

    return data_view(
        request, data= filter.qs,
        data_template='payment/index.html', 
        table_headers=['S/N', 'Amount', 'Paid On', 'RRR', 'Verified?'],
        filter_form = filter.form, title='Payments',
    )

@login_required
def registration_fee(request):
    amount = float(Board().registration_fee)

    if is_post(request):
        verification_url = reverse('payment:verify-reg-fee-payment')
        verification_url = request.build_absolute_uri(verification_url)
        url = payment.url(amount, request.user, verification_url)

        return redirect(url)

    return render(
        request, 'payment/registration-fee',
        title = 'Registration FEE Payment',
        amount = amount
    )


@login_required
def verify_reg_fee_payment(request):
    rrr = request.GET.get('reference', None)
    
    if rrr is not None:
        amount = Board().registration_fee
        payment_verified = payment.verify(ref=rrr, amount=amount)

        if payment_verified:
            payment_obj, _ = Payment.objects.get_or_create(
                amount=amount, payment_type = 1, rrr=rrr
            )
            
            request.user.registration_fee_payment = payment_obj
            request.user.save()

            messages.success(request, 'Registration FEE paid successfully!!!')
            messages.info(request, 'Please complete your profile information.')
            return redirect('applicant:profile')

    return render(request, 'payment/verify-payment', title='BSSB Verify Payment')

@complete_profile_required
def application_fee(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    amount = float(scholarship.application_fee)

    if is_post(request):
        application = Application.get_or_create(request.user, scholarship)
        verification_url = reverse('payment:verify-app-fee-payment', kwargs={'id':application.id})
        verification_url = request.build_absolute_uri(verification_url)
        url = payment.url(amount, request.user, verification_url)
        return redirect(url)

    return render(
        request, 'payment/application-fee',
        title='Pay Registration Fee',
        scholarship = scholarship,
    )
    
@complete_profile_required
def verify_application_fee(request, id):
    application:Application = get_object_or_404(Application, id=id)
    
    rrr = request.GET.get('reference', None)
    
    if rrr is not None:
        scholarship:Scholarship = application.scholarship
        amount = scholarship.application_fee
        payment_verified = payment.verify(ref=rrr, amount=amount)

        if payment_verified:
            payment_obj, _ = Payment.objects.get_or_create(
                amount=amount,
                payment_type = 2,
                rrr=rrr
            )
            application.application_fee_payment = payment_obj
            application.save()

            messages.success(request, 'Application FEE paid successfully!!!')
            messages.info(request, 'Please review your profile details and then upload the required documents.')
            return redirect('applicant:apply', id=scholarship.id)

    return render(request, 'payment/verify-payment', title='BSSB Verify Payment')