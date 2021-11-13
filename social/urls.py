from django.urls import path
from .views import *
from paymentgateway.views import *
urlpatterns = [
    path('', AllPostView.as_view(), name="all-post"),
    path('make-post/', MakePost.as_view(), name="make-post"),
    path('profile/<int:pk>/', ProfileView.as_view(), name="profile"),
    path('post-detail/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post-delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/',
         CommentDeleteView.as_view(), name='comment-delete'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile-edit'),
    path('profile/<int:pk>/connections/add',
         AddConnection.as_view(), name='add-connection'),
    path('profile/<int:pk>/connections/remove',
         RemoveConnection.as_view(), name='remove-connection'),
    path('search/', Search.as_view(), name="search"),

    # payment ------------
    path('payment/<int:pk>/', home, name='payment-home'),
    path('transaction-details/<int:pk>/',
         ViewTranasactionDetails.as_view(), name='trans-details'),
]
