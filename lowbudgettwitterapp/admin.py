
from django.contrib import admin
from .models import Account, Tweet, Following, Reply

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ('password',)


admin.site.register(Account, AccountAdmin)
admin.site.register(Following)
admin.site.register(Tweet)
admin.site.register(Reply)