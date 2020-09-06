from django.db import models
import datetime

import django.utils.timezone as date
# Create your models here.


class Prediction(models.Model):

    date = models.DateField(default=date.now())
    value = models.FloatField(default=0.0)

    def __str__(self):

        return str(self.date) + str(self.value)





    