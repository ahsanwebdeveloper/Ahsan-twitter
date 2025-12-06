from django.urls import path
from . import views

urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('tweet/<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
   path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
   path('register/', views.registration, name='register'),
   path("<int:id>/like/", views.like_tweet, name="like_tweet"),
   path("<int:id>/comment/", views.comment_tweet, name="comment_tweet"),
   path("live-search/", views.live_search, name="live_search"),
   path('user/<str:username>/', views.profile_view, name='profile'),


]
