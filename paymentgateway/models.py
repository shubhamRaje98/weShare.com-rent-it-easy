from django.db import models
from social.models import *
from django.contrib.auth.models import User

# Create your models here.


class TransactionDetails(models.Model):
    rentee = models.ForeignKey(User, on_delete=models.CASCADE)
    trans = models.IntegerField(default=1)
    product = models.CharField(max_length=200, default="")
    renter = models.CharField(max_length=200, default="")
    subPeriod = models.IntegerField(default=3)
    monthlyCharge = models.IntegerField(default=100)
    deposite = models.IntegerField()
    address = models.CharField(max_length=300)
    order_id = models.CharField(max_length=100, default="failed")

    def __str__(self):
        return '%s %s' % (self.product, self.renter)
