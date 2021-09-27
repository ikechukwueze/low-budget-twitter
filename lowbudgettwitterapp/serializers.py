from rest_framework import serializers
from .models import Account, Tweet



class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['username', 'display_name', 'profile_pic', 'following_count', 'followers_count']



class TweetSerializer(serializers.ModelSerializer):
    author = AccountSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['author', 'id', 'tweet', 'formatted_date_time', 'likes', 'retweets']