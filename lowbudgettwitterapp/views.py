import json
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm, SignUpForm, SignInForm
from .models import Account, Following, Tweet

from .serializers import TweetSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


# Create your views here.


def sign_in_view(request):
    sign_in_form = SignInForm()
    if request.method == "POST":
        sign_in_form = SignInForm(request.POST)
        if sign_in_form.is_valid():
            username = sign_in_form.cleaned_data.get("username")
            password = sign_in_form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("time_line")
    return render(request, "lowbudgettwitterapp/sign-in.html", {"signinform": sign_in_form})



def sign_up_view(request):
    sign_up_form = SignUpForm()
    if request.method == "POST":
        sign_up_form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            sign_up_form.save()
            username = sign_up_form.cleaned_data.get("username")
            password = sign_up_form.cleaned_data.get("password1")
            authenticated_user = authenticate(request, username=username, password=password)
            #Following.objects.create(account=Account)
            #new_account.following.add(new_user)
            login(request, authenticated_user)
            return redirect("time_line")
    return render(request, "lowbudgettwitterapp/sign-up.html", {"signupform": sign_up_form})



def sign_out_view(request):
    logout(request)
    return redirect("sign_in")



@login_required(login_url="sign_in")
def time_line(request):
    account = Account.objects.get(username=request.user)
    f = Following.objects.get(account=account)
    following = f.following.count() - 1
    followers = f.followers.count()
    #tweets = Tweet.objects.filter(author__in=f.following.all())
    profile_form = ProfileForm(
        initial={"display_name": account.display_name, "bio": account.bio}
    )

    return render(
        request,
        "lowbudgettwitterapp/index.html",
        {
            "profileform": profile_form,
            "account": account,
            "follower_count": followers,
            "following_count": following,
        },
    )



def update_profile(request):
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            account = Account.objects.get(username=request.user)
            account.display_name = profile_form.cleaned_data.get("display_name")
            account.bio = profile_form.cleaned_data.get("bio")
            img = request.FILES.get("profile_pic", None)
            if img is not None:
                account.profile_pic = img
            account.save()
        return redirect("time_line")



@api_view(["GET", "POST"])
def get_or_post_tweets_endpoint(request):
    following = Following.objects.get(account=request.user).following.all()
    global most_recent_tweet
    if request.method == "GET":
        all_tweets = Tweet.objects.filter(author__in=following)
        most_recent_tweet = all_tweets[0]
        print(most_recent_tweet)
        serializer = TweetSerializer(all_tweets, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = TweetSerializer(data=request.data)
        if serializer.is_valid():
            tweet = serializer.validated_data["tweet"]
            posted_tweet = Tweet.objects.create(author=request.user, tweet=tweet)
            new_tweets = (
                Tweet
                .objects
                .all()
                .filter(
                    author__in=following,
                    date_time__gt=most_recent_tweet.date_time,
                    date_time__lte=posted_tweet.date_time
                )
            )
            serializer = TweetSerializer(new_tweets, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def like_or_retweet_endpoint(request):
    if request.method == "POST":
        body = request.body.decode('utf-8')
        body = json.loads(body)
        tweet_id = body['tweet_id']
        action = body['action']
        like_update = body['like_update']
        print(action)
        liked_by = UserProfile.objects.get(user=request.user)
        
        tweet = Tweet.objects.get(pk=tweet_id)
        tweet.likes += like_update
        if like_update > 0:
            tweet.liked_by.add(liked_by)  #has to be userprofile
        else:
            tweet.liked_by.remove(liked_by)
        tweet.save()
        
        data = {'like_count':tweet.likes}
        return JsonResponse(data)