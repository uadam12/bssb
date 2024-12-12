from django.db import models
from django.urls import reverse_lazy, reverse
from users.models import User

# Create your models here.
class Ticket(models.Model):
    name = models.CharField(max_length=100)
    is_resolved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    list_url = reverse_lazy('support:tickets')
    add_url = reverse_lazy('support:create-ticket')

    @property
    def url(self):
        return reverse('support:ticket', kwargs={'id':self.pk})
    
    @property
    def resolve_url(self):
        return reverse('support:ticket-resolve', kwargs={'id':self.pk})

    def __str__(self) -> str:
        return f"Ticket #{self.pk}: {self.name} from {self.user}"

    class Meta:
        ordering = ['-created_on', 'name']


class Message(models.Model):
    content = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complains')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    list_url = reverse_lazy('support:messages')
    add_url = reverse_lazy('support:create-message')
    
    def clean(self) -> None:
        super().clean()

    def __str__(self) -> str:
        return f"{self.ticket.name}: {self.content[:30]}..."
    
    class Meta:
        ordering = ['sent_on', 'content']