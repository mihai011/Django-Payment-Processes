from django.db import models
from django.utils import timezone

import payments.validators as validators
# Create your models here.


class Payment(models.Model):

    creditcardnumber = models.CharField(max_length=16, validators=[validators.creditcard_validator])
    cardholder = models.CharField(max_length=50)
    expirationdate = models.DateField(validators=[validators.date_validator])
    securitycode = models.CharField(blank=True, null=True, max_length=3, validators=[validators.security_validator])
    amount = models.IntegerField(validators=[validators.amount_validator])

    #execution time of the payment
    executiontime = models.DateTimeField(default=timezone.now())