from django.db import models
from django.urls import reverse, reverse_lazy
from app import compress
from users.models import User


# Create your models here.
class Article(models.Model):
    headline = models.CharField(max_length=100)
    headline_image = models.ImageField(default='/headline.png', upload_to='headline-images', blank=True)
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    publish_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    add_url = reverse_lazy('main:create-article')
    list_url = reverse_lazy('main:articles')

    @property
    def url(self):
        return reverse('main:article', kwargs={'id':self.pk})
    
    @property
    def update_url(self):
        return reverse('main:update-article', kwargs={'id':self.pk})
    
    @property
    def delete_url(self):
        return reverse('main:delete-article', kwargs={'id':self.pk})
    
    @property
    def contents(self):
        res = self.content.split('\n')
        return [i.strip() for i in res]
    
    def save(self, *args, **kwargs):
        try:
            self.picture = compress(self.headline_image)
        except: pass
        
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.headline
    
    class Meta:
        ordering = ('-publish_on', 'headline')

class FAQ(models.Model):
    question = models.CharField(unique=True, max_length=150)
    answer = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    add_url = reverse_lazy('main:create-faq')
    list_url = reverse_lazy('main:faqs')
    
    @property
    def update_url(self):
        return reverse('main:update-faq', kwargs={'id':self.pk})
    
    @property
    def url(self):
        return reverse('main:faq', kwargs={'id':self.pk})
    
    @property
    def delete_url(self):
        return reverse('main:delete-faq', kwargs={'id':self.pk})
    
    def __str__(self):
        return self.question[:50]

class Contact(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    send_on = models.DateField(auto_now_add=True)
    
    @property
    def reply_url(self):
        return reverse('main:reply', kwargs={'contact_id':self.pk})

    def __str__(self) -> str:
        return f"{self.sender}: {self.message[:30]}"

    class Meta:
        ordering = ('-send_on', )
        
class Notification(models.Model):
    VISIBILITIES = (
        ('public', 'Public'),
        ('members', 'Members only'),
        ('selected', 'Selected members')
    )
    
    message = models.CharField(max_length=255)
    notified_at = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITIES, default='members')
    users = models.ManyToManyField(User, blank=True, related_name='notifications')
    
    add_url = reverse_lazy('main:create-notification')
    list_url = reverse_lazy('main:notifications')

    @property
    def url(self):
        return reverse('main:notification', kwargs={'id':self.pk})
    
    @property
    def update_url(self):
        return reverse('main:update-notification', kwargs={'id':self.pk})
    
    @property
    def delete_url(self):
        return reverse('main:delete-notification', kwargs={'id':self.pk})

    def __str__(self) -> str:
        return self.message[:50]
    
    class Meta:
        ordering = ['-notified_at', 'message']