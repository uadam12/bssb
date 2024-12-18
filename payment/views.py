from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from app import render, is_post
from app.views import data_view
from app.auth import login_required, officials_only, complete_profile_required
from board.models import Board
from scholarship.models import Scholarship, Application
from users.models import User
from .filters import PaymentFilter
from .payment import remita
from .models import Payment


# Create your views here.
@officials_only(main_admin_only=True)
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
    user:User = request.user
    amount = Board.load().registration_fee
    payment:Payment = Payment.objects.filter(amount=amount, payment_type=1, email=user.email).first()
    
    if payment is None:
        payment_description = f'Registration FEE Payment from {user}'
        payment_info = remita.init_payment(
            description=payment_description,
            totalAmount=amount,
            user=user,
        )

        if payment_info.get("statuscode") == "025":
            rrr = payment_info.get('RRR')
            payment = Payment(
                rrr=rrr, payment_type=1, 
                email=user.email, amount=amount,
                description=payment_description,
            )
            payment.save()
        else: messages.error(request, 'Something went wrong. Please refresh the page.')

    elif user.registration_fee_payment.pk == payment.pk and payment.verified:
        messages.info(request, 'Registration FEE paid already.')
        return redirect(user.profile)

    if is_post(request): return redirect(payment.url)

    return render(
        request, 'payment/registration-fee',
        title='Registration FEE Payment',
        payment=payment
    )


@login_required
def verify_reg_fee_payment(request):
    rrr = request.GET.get('rrr', None)
    payment:Payment = Payment.objects.filter(payment_type=1, rrr=rrr).first()
    
    if payment is None:
        return redirect('payment:registration-fee')

    if rrr and not payment.verified:
        user:User = request.user
        payment_info = remita.verify_payment(rrr=rrr)

        if payment_info.get('status') in ['00', '01']:
            if payment_info.get('payerEmail') == user.email:
                payment.verified = payment.amount >= Board.load().registration_fee
                user.registration_fee_payment = payment
                payment.save()
                user.save()

                messages.success(request, 'Registration FEE paid successfully!!!')
                messages.info(request, 'Please complete your profile information.')
                return redirect(user.profile)
            messages.error(request, 'Payment details not found')

    return render(request, 'payment/verify-payment', title='Verify registration fee payment')

@complete_profile_required
def application_fee(request, id):
    applicant:User = request.user
    scholarship = get_object_or_404(Scholarship, id=id)
    amount = scholarship.application_fee
    application = Application.get_or_create(applicant, scholarship)
    app_payment = application.application_fee_payment
    
    if app_payment is None:
        payment_description = f'Application FEE Payment of {scholarship} from {applicant}'
        payment_info = remita.init_payment(
            description=payment_description,
            totalAmount=amount,
            user=applicant,
        )

        if payment_info.get("statuscode") == "025":
            rrr = payment_info.get('RRR')
            app_payment = Payment(
                amount=amount, 
                email=applicant.email,
                payment_type=1, rrr=rrr, 
                description=payment_description
            )
            app_payment.save()
            application.application_fee_payment = app_payment
            application.save()
        else: messages.error(request, 'Something went wrong. Please refresh the page.')

    elif app_payment and app_payment.verified:
        messages.info(request, f"Application FEE for {scholarship} paid already.")
        return redirect(applicant.dashboard)    

    if is_post(request): return redirect(app_payment.url)

    return render(
        request, 'payment/application-fee',
        title='Pay Application FEE',
        application = application,
        scholarship = scholarship,
        payment = app_payment
    )
    
@complete_profile_required
def verify_application_fee(request, id):
    application:Application = get_object_or_404(Application, id=id)
    scholarship:Scholarship = application.scholarship
    payment = application.application_fee_payment
    rrr = request.GET.get('rrr', None)

    if payment is None:
        return redirect('payment:application-fee', kwargs={'id': scholarship.pk})

    if rrr and not payment.verified:
        applicant:User = request.user
        payment_info = remita.verify_payment(rrr=rrr)

        if payment_info.get('status') in ['00', '01']:
            if payment_info.get('payerEmail') == applicant.email:
                payment.verified = payment.amount >= scholarship.application_fee
                application.application_fee_payment = payment
                payment.save()
                application.save()

                messages.success(request, 'Application FEE paid successfully!!!')
                messages.info(request, 'Please review your profile details and then upload the required documents.')
                return redirect('applicant:apply', id=scholarship.id)
            messages.error(request, 'Payment details not found')
    return render(request, 'payment/verify-payment', title='BSSB Verify Payment')