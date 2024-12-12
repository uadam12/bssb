from django.urls import path
from . import views

app_name = 'main'


urlpatterns = [
    path('', views.index, name='home'),
    path('news/', views.news, name='news'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_us, name='contact'),
    path('reply/<int:contact_id>/', views.reply, name='reply'),

    # Frequently Asked Questions(FAQs)
    path('faqs/', views.faqs, name='faqs'),
    path('faqs/<int:id>/', views.faq, name='faq'),
    path('faqs/create/', views.create_faq, name='create-faq'),
    path('faqs/<int:id>/update/', views.update_faq, name='update-faq'),
    path('faqs/<int:id>/delete/', views.delete_faq, name='delete-faq'),
    
    # Contacts and Notifications
    path('contacts/', views.contacts, name='contacts'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/all', views.all_notifications, name='all-notifications'),
    path('notifications/create/', views.create_notification, name='create-notification'),
    path('notifications/<int:id>/update/', views.update_notification, name='update-notification'),
    path('notifications/<int:id>/delete/', views.delete_notification, name='delete-notification'),
    
    # Articles
    path('articles/', views.articles, name='articles'),
    path('news/<int:id>', views.article, name='article'),
    path('articles/create', views.create_article, name='create-article'),
    path('articles/<int:id>/update', views.update_article, name='update-article'),
    path('articles/<int:id>/delete', views.delete_article, name='delete-article'),
]
