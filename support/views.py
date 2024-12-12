from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from app import render, is_htmx, is_post
from app.auth import applicant_only, officials_only, login_required
from app.views import data_view, create_view, trigger
from main.models import Notification
from .forms import TicketForm, MessageForm, TicketFilter
from .models import Ticket, Message, User

def notify(message:str, owner:User, user:User):
    users = User.objects.filter(
        Q(access_code__gt = 2) |
        Q(access_code = 1) & Q(pk=owner.pk)
    ).exclude(pk=user.pk)

    notification = Notification.objects.create()
    notification.message = message
    notification.visibility = 'selected'
    notification.users.set(users)
    notification.save()
    


# Create your views here.
@officials_only(admin_only=True)
def index(request):
    filter = TicketFilter(request.GET)
    
    return data_view(
        request, filter.qs,
        data_template='support/index.html',
        filter_form=filter.form, title='Tickets',
        table_headers=['S/N', 'Ticket', 'Owner Email', 'Open on', 'Is Resolve', 'Action']
    )

@applicant_only
def tickets(request):
    return data_view(
        request=request,
        table_headers=['S/N', 'Ticket Name', 'Status', 'View'],
        data=Ticket.objects.filter(user=request.user).all(),
        data_template='support/applicant-tickets.html',
        add_url=Ticket.add_url, title='My Tickets'
    )

@applicant_only
def create_ticket(request):
    user = request.user
    def save(ticket:Ticket):
        ticket.user = user
        ticket.save()
        
        message = f"A new ticket is created by {user}"
        notify(message, owner=user, user=user)

    return create_view(
        request=request,
        form_class=TicketForm,
        success_url=Ticket.list_url,
        save_instantly=False,
        further_action=save,
        form_header='Create new ticket'
    )

@applicant_only
def ticket_resolve(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    user:User = request.user
    
    if user.pk != ticket.user.pk:
        messages.info(request, 'Only admin or the owner can view ticket.')
    elif not ticket.is_resolved:
        ticket.is_resolved = True
        ticket.save()
        message = f"{ticket} of {user} is resolved"
        notify(message, owner=user, user=user)
        
    messages.info(request, f"{ticket} resolved")
    
    return render(request, 'parts/ticket-status', ticket=ticket)
    
@login_required
def ticket(request, id:int):
    ticket = get_object_or_404(Ticket, id=id)
    user:User = request.user

    if user.access_code < 3 and user.pk != ticket.user.pk:
        messages.info(request, 'Only admin or the owner can view ticket.')

    form = MessageForm()
    
    if is_post(request):
        form = MessageForm(request.POST)

        if form.is_valid():
            message:Message = form.save(False)
            message.sender = request.user
            message.ticket = ticket
            message.save()
            
            message = f"New message from {user} on {ticket}"
            notify(message, owner=ticket.user, user=user)

            if is_htmx(request):
                ticket_messages = Message.objects.filter(ticket=ticket).all()
                response = render(request, 'parts/tickets', data=ticket_messages)
                trigger(response, 'message-sent')
                return response

            messages.success(request, 'Message sent')
    
    ticket_messages = Message.objects.filter(ticket=ticket).all()

    if is_htmx(request):
        return render(request, 'parts/tickets', data=ticket_messages)

    return render(
        request, 'support/ticket', 
        title=str(ticket), form=form,
        data=ticket_messages, ticket=ticket,
        with_htmx=True
    )