from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_resized import ResizedImageField


# Create your models here.



class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('User must have a username')
        
        if not email:
            raise ValueError('User must have an email address')
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
		)
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
			email=self.normalize_email(email),
			password=password,
		)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    
    display_name = models.CharField(max_length=20, blank=True)
    bio = models.TextField(max_length=100, blank=True)
    profile_pic = ResizedImageField(
        size=[300, 300],
        crop=['middle', 'center'],
        upload_to='profile_pictures',
        blank=True,
        null=True,
        default='default_profile_pic.jpg'
    )
    following_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)

    date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
	
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
	    return self.is_admin
        
    def has_module_perms(self, app_label):
        return True
    
    def profile_pic_url(self):
        try:
            url = self.profile_pic.url
        except:
            url = settings.MEDIA_URL + 'default_profile_pic.jpg'
        return url



"""
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users')
    username = models.CharField(max_length=20, blank=True)
    display_name = models.CharField(max_length=20, blank=True)
    #profile_pic = models.ImageField(upload_to='profile_pictures', blank=True, default='default_profile_pic.jpg')
    profile_pic = ResizedImageField(size=[300, 300], crop=['middle', 'center'], upload_to='profile_pictures', blank=True, null=True, default='default_profile_pic.jpg')
    bio = models.TextField(max_length=100, blank=True)
    following = models.ManyToManyField(User, blank=True, related_name='following')
    followers = models.ManyToManyField(User, blank=True, related_name='followers')


    def __str__(self):
        return self.username
    
    @property
    def profile_pic_url(self):
        try:
            url = self.profile_pic.url
        except:
            url = settings.MEDIA_URL + 'default_profile_pic.jpg'
        return url
"""


class Following(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='accounts')
    following = models.ManyToManyField(Account, related_name='followings')
    followers = models.ManyToManyField(Account, related_name='followers')

    def __str__(self):
        return self.account


class Tweet(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='tweets')
    tweet = models.TextField(max_length=280, blank=False, null=False)
    date_time = models.DateTimeField(auto_now=True)
    formatted_date_time = models.CharField(max_length=50, blank=True, null=True)
    
    is_retweet = models.BooleanField(default=False)
    is_reply = models.BooleanField(default=False)
    likes = models.IntegerField(blank=True, null=True, default=0)
    retweets = models.IntegerField(blank=True, null=True, default=0)
    
    liked_by = models.ManyToManyField(Account, blank=True, related_name='liked_tweets')
    retweeted_by = models.ManyToManyField(Account, blank=True, related_name='retweeted_tweets')


    class Meta:
        ordering = ['-date_time']
    
    def __str__(self):
        return f'{self.author} - {self.tweet[:10]}' 



class Reply(Tweet):
    referenced_tweet = models.ForeignKey(Tweet, on_delete=models.PROTECT, related_name='replies')
    
    class Meta:
        verbose_name_plural = 'Replies'


"""
class PrivateMessage(models.Model):
    message = models.TextField(max_length=280, blank=False, null=False)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages')
    date_time = models.DateTimeField(auto_now=True)
"""


# post save method for Tweet
@receiver(post_save, sender=Tweet)
def format_tweet_date(sender, instance, created, **kwargs):
    date_time_format = '%H:%M · %d %b %Y'
    if created:
        instance.formatted_date_time = instance.date_time.strftime(date_time_format)
        instance.save()