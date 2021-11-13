from django.shortcuts import render, redirect
import razorpay
from django.views.decorators.csrf import csrf_exempt
from weShare.settings import razorpay_id, razorpay_secret_key
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from social.models import *
from social.forms import *

from .models import TransactionDetails
from social.models import UserProfile

from weShare.settings import TRANSACTION_HAPPEND

client = razorpay.Client(auth=(razorpay_id, razorpay_secret_key))


def home(request, pk):
    rentee = UserProfile.objects.get(user=request.user)
    renteeName = rentee.user
    renteeLocation = rentee.location
    renteePhone = rentee.phoneNo
    renteeEmail = rentee.emailId

    post = Post.objects.get(pk=pk)
    renter = post.author
    address = rentee.location
    product = post.productName
    subPeriod = post.subscriptionPeriod
    montlycharge = post.productMonthlyCharge
    loc = rentee.location
    order_amount = post.deposite*100

    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    notes = {'Shipping address': 'Bommanahalli, Bangalore'}   # OPTIONAL

    payment_order = client.order.create(
        dict(amount=order_amount, currency=order_currency, payment_capture=1))
    payment_order_id = payment_order['id']

    createTransaction(request, rentee, pk, payment_order_id)

    post.rented = True
    post.save()

    context = {
        'razorpay_id': razorpay_id,
        'order_id': payment_order_id,
        'razorpay_secret_key': razorpay_secret_key,
        'renter': renter,
        'product': product,
        'subPeriod': subPeriod,
        'montlycharge': montlycharge,
        'order_amount': order_amount/100,
        'rented': post.rented,
        'address': address,
        'renteePhone': rentee.phoneNo,
        'renteeEmail': rentee.emailId,
        'renteeName': rentee.user,


    }
    return render(request, 'paymentgateway/index.html', context)


def createTransaction(request, rentee, pk, payment_order_id):
    post = Post.objects.get(pk=pk)
    renter = post.author
    product = post.productName
    subPeriod = post.subscriptionPeriod
    montlycharge = post.productMonthlyCharge
    loc = rentee.location
    order_amount = post.deposite*100


    # Inserting data in TrasactionDetails object
    transaction = TransactionDetails(rentee=request.user, trans=pk, product=product, renter=renter, subPeriod=subPeriod,
                                     monthlyCharge=montlycharge, deposite=order_amount, address=loc, order_id=payment_order_id)

    transaction.save()
