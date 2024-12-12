from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from board.models import Board
from app import render, is_post
from app.auth import login_required
from app.context_processors import get_notifications
from app.views import create_view, update_view, delete_view, data_view
from .models import FAQ, Article, Notification, Contact
from .forms import FAQForm, ArticleForm, ContactForm, NotificationForm
from .filters import FAQFilter, ArticleFilter, ContactFilter, NotificationFilter


# Frequently Asked Questions(FAQs)
def faqs(request):
    filter = FAQFilter(request.GET, queryset=FAQ.objects.all())

    return data_view(
        request, data_template='main/faqs.html',
        data=filter.qs, filter_form=filter.form,
        table_headers=['S/N', 'Question', 'Answer', 'Actions'],
        add_url=reverse('main:create-faq'), title='FAQs'
    )

def create_faq(request):
    return create_view(
        request, form_class=FAQForm, 
        success_url='main:faqs', 
        form_header='Add Frequently Asked Questions(FAQ)'
    )
    
def faq(request, id):
    faq = get_object_or_404(FAQ, id=id)
    
    return render(
        request, 'main/faq', faq
    )

def update_faq(request, id):
    faq = get_object_or_404(FAQ, id=id)
    
    return update_view(
        request, FAQForm, 
        faq, "Update Frequently Asked Questions(FAQ)", 
        save_instantly=True
    )

def delete_faq(request, id):
    faq = get_object_or_404(FAQ, id=id)
    
    return delete_view(
        request, faq, "Delete Frequently Asked Question(FAQ)"
    )
    
# Notifications
def notifications(request):
    filter = NotificationFilter(request.GET, queryset=Notification.objects.all())

    return data_view(
        request, data_template='main/notifications.html',
        data=filter.qs, filter_form=filter.form,
        table_headers=['S/N', 'Message', 'Visibility', 'Actions'],
        add_url=reverse('main:create-notification'), title='Notifications'
    )

def create_notification(request):
    return create_view(
        request, form_class=NotificationForm, 
        success_url='main:notifications', 
        form_header='Add notification'
    )

def update_notification(request, id):
    notification = get_object_or_404(Notification, id=id)
    
    return update_view(
        request, NotificationForm, 
        notification, "Update notification", 
        save_instantly=True
    )

def delete_notification(request, id):
    notification = get_object_or_404(Notification, id=id)
    
    return delete_view(
        request, notification, "Delete notification"
    )

def index(request):
    board = Board()
    faqs = FAQ.objects.all()
    return render(request, 'main/index', board=board, faqs=faqs)

def news(request):
    articles = Article.objects.all()
    pagenator = Paginator(articles, 10, 4)
    page = request.GET.get('page', 1)
    articles = pagenator.get_page(page)
    
    return render(request, 'main/news', articles=articles)

def about(request):
    return render(request, 'main/about', abouts=Board.load().abouts)

@login_required
def contact_us(request):
    if is_post(request):
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            
            messages.success(request, 'Message sent successfully!')
            return redirect(request.user.dashboard)
    else:form = ContactForm()
    
    return render(request, 'main/contact', form=form)

def all_notifications(request):
    if is_post(request):
        if request.user.is_authenticated:
            request.user.last_time_read_notifications = timezone.now()
            request.user.save()
            messages.success(request, 'Mark as read successfully.')
            return redirect(request.path)

    return render(
        request, 'main/all-notifications', 'All Notifications',
        data = get_notifications(request.user)
    )

def reply(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    return create_view(
        request, submit_text='Reply',
        form_class=NotificationForm, 
        success_url='main:notifications', 
        form_header=f"Reply on: {contact.subject}"
    )

def contacts(request):
    filter = ContactFilter(request.GET, queryset=Contact.objects.all())

    return data_view(request, 
        data_template='main/contacts.html',
        data=filter.qs, filter_form=filter.form,
        main_template='main/all_contacts', title='Contacts',
        table_headers=['S/N', 'Subject', 'Message', 'Actions'],
    )


# Articles
def articles(request):
    filter = ArticleFilter(request.GET, queryset=Article.objects.all())

    return data_view(
        request,
        title='Articles/News',
        add_url=Article.add_url,
        data_template="main/articles.html",
        data=filter.qs, filter_form=filter.form,
        table_headers=['S/N', 'Headline', 'Published on', 'Updated on', 'Actions']
    )
    
def article(request, id):
    article = get_object_or_404(Article, id=id)
    return render(
        request, 'main/article',
        title = article.headline,
        article = article
    )

def create_article(request):
    return create_view(
        request, form_class=ArticleForm, 
        success_url='main:articles', 
        form_header='Create Article'
    )

def update_article(request, id):
    article = get_object_or_404(Article, id=id)

    return update_view(
        request, instance=article,
        form_class=ArticleForm, 
        form_header='Update Article'
    )
    
def delete_article(request, id):
    article = get_object_or_404(Article, id=id)
    return delete_view(request, model=article, header='Delete Article')