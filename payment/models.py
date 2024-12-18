from django.db import models


# Create your models here.
class Payment(models.Model):
    TYPES = ((1, 'Registration FEE'), (2, 'Application FEE'), (3, 'Disbursement'))

    amount = models.PositiveIntegerField()
    rrr = models.CharField(max_length=20, unique=True)
    email=models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    payment_type = models.PositiveSmallIntegerField(choices=TYPES, default=1)
    paid_on = models.DateField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    
    @property
    def url(self):
        return f"https://demo.remita.net/remita/onepage/biller/{self.rrr}/payment.spa"

    def __str__(self) -> str:
        return f"Payment of N{self.amount} on {self.paid_on}"
    
    class Meta:
        ordering = ('-paid_on', )
