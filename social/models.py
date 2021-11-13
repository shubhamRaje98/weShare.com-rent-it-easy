# weShare Models

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    PRODUCT_CATAGORY = (
        ("Electronics", "Electronics"),
        ("Clothing", "Clothing"),
        ("Vehicle", "Vehicle"),
        ("Fashion", "Fashion"),
        ("Education", "Education"),
    )

    subPlan = (
        (3, 3),
        (6, 6),
        (12, 12),
        (24, 24),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    productDesc = models.CharField(
        max_length=500, default="It's a good product truly")
    productName = models.CharField(max_length=100)
    productCategory = models.CharField(
        max_length=100, choices=PRODUCT_CATAGORY)
    productMonthlyCharge = models.IntegerField(default=100)
    productImage = models.FileField(
        upload_to='uploads/products', default='uploads/products/skillengineering.jpg', blank=True, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(
        User, blank=True, related_name='dislikes')
    deposite = models.IntegerField(default=100)
    subscriptionPeriod = models.IntegerField(default=3, choices=subPlan)
    rented = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s' % (self.author, self.created_on)


class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile',
                                default="I yet to set up my profile!", on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(max_length=200, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    picture = models.ImageField(
        upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.png')
    followers = models.ManyToManyField(
        User, blank=True, related_name='followers')
    location = models.CharField(max_length=100, default="")
    emailId = models.EmailField(default='example@gmail.com')
    phoneNo = models.BigIntegerField(default=0)


'''
class TransactionDetails(models.Model):
    deliveryAddress = models.CharField(max_length=100, default="")
    product = models.CharField(max_length=200)
    renter = models.CharField(max_length=100)
    rentee = models.CharField(max_length="")
    transactionDeposite = models.Int
'''


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
