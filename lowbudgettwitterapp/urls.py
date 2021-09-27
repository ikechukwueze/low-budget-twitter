from django.urls import path
from . import views


urlpatterns = [
    path('', views.time_line, name='time_line'),
    path('signin/', views.sign_in_view, name='sign_in'),
    path('signup/', views.sign_up_view, name='sign_up'),
    path('signout/', views.sign_out_view, name='sign_out'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('get-post-tweets/', views.get_or_post_tweets_endpoint, name="get_or_post_tweets"),
    path('like-or-retweet/', views.like_or_retweet_endpoint, name="like_or_retweet"),
]
