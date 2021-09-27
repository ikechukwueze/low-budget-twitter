# Generated by Django 3.2.6 on 2021-09-25 17:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lowbudgettwitterapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('following', models.ManyToManyField(related_name='followings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]