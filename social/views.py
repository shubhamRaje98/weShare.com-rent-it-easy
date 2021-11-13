from django.db.models.query_utils import Q
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import *
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from weShare.settings import TRANSACTION_HAPPEND
from paymentgateway.models import TransactionDetails
from math import ceil
# Create your views here.


class AllPostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        allProds = []
        catprods = Post.objects.values('productCategory')
        cats = (item['productCategory'] for item in catprods)
        for cat in cats:
            prod = Post.objects.filter(productCategory=cat)
            n = len(prod)
            nslides = n//4 + ceil((n/4)-(n//4))
            allProds.append([prod, range(1, nslides), nslides])

        context = {'allProds': allProds}
        paginate_by = 6
        return render(request, "social/all-post.html", context)


class MakePost(View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        context = {'form': form}
        return render(request, "social/make-post.html", context)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

            return redirect("/social/")

        context = {
            'form': form,
        }

        return render(request, "social/make-post.html", context)


class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by("-created_on")
        followers = profile.followers.all()

        if len(followers) == 0:
            is_following = False
        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        number_of_followers = len(followers)

        context = {
            'profile': profile,
            'user': user,
            'posts': posts,
            'number_of_followers': number_of_followers,
            'is_following': is_following,
        }

        return render(request, "social/profile.html", context)


class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        form = CommentForm()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'transaction_status': post.rented,
        }

        return render(request, "social/post-details.html", context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)
        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            "post": post,
            "form": form,
            "comments": comments,
        }

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

            return redirect("/social/")

        return render(request, "social/post-details.html", context)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'social/post-delete.html'
    success_url = reverse_lazy('all-post')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'social/comment-delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    template_name = 'social/profile-edit.html'
    fields = ['name', 'birth_date', 'emailId',
              'phoneNo', 'location', 'bio', 'picture']

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user


class AddConnection(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)

        return redirect('profile', pk=profile.pk)


class RemoveConnection(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect('profile', pk=profile.pk)


class Search(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains=query)
        )
        context = {
            'profile_list': profile_list,
        }
        return render(request, 'social/search.html', context)


class ViewTranasactionDetails(View):
    def get(self, request, pk, *args, **kwargs):
        transactionData = TransactionDetails.objects.filter(trans=pk)
        print("The pk is : " + str(pk))
        print("The rentee is : " + str(transactionData[0].rentee))

        # Data to pass
        product = transactionData[0].product
        renter = transactionData[0].renter
        rentee = transactionData[0].rentee
        deposite = transactionData[0].deposite
        subscriptionPlan = transactionData[0].subPeriod
        monthlyCharge = transactionData[0].monthlyCharge
        orderId = transactionData[0].order_id
        address = transactionData[0].address

        context = {
            'product': transactionData[0].product,
            'renter': transactionData[0].renter,
            'rentee': transactionData[0].rentee,
            'deposite': transactionData[0].deposite/100,
            'subscriptionPlan': transactionData[0].subPeriod,
            'monthlyCharge': transactionData[0].monthlyCharge,
            'orderId': transactionData[0].order_id,
            'address': transactionData[0].address,
            'transactionData': transactionData,
        }

        return render(request, 'social/transDetail.html', context)
