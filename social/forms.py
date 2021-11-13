from django import forms
from django.db.models import fields
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['productName', "productCategory",
                  "productMonthlyCharge", "productDesc", "deposite", "subscriptionPeriod", "productImage"]

    productName = forms.CharField(
        label='Product Name ',
        widget=forms.Textarea(attrs={
            'rows': '1',
            'placeholder': ' Enter the descriptive name of your product...'
        })


    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    comment = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '2',
            'placeholder': 'comment..'
        })
    )


# ************************
