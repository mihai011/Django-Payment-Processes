from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from http import HTTPStatus


import payments.validators as validators
from payments.dispatcher import Dispatcher
# Create your models here.


class Payment(models.Model):

    creditcardnumber = models.CharField(max_length=16, validators=[validators.creditcard_validator])
    cardholder = models.CharField(max_length=50)
    expirationdate = models.DateField(validators=[validators.date_validator])
    securitycode = models.CharField(blank=True, null=True, max_length=3, validators=[validators.security_validator])
    amount = models.IntegerField(validators=[validators.amount_validator])

    #execution time of the payment
    executiontime = models.DateTimeField(default=timezone.now())


@receiver(post_save, sender=Payment)
def send_payment(sender, instance, **kwargs):

    #dispatch payment to Dispatcher class
    payment = model_to_dict(instance)
    Dispatcher.dispatch.delay(payment)  



        