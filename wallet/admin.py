from django.contrib import admin

from wallet.models import PurseModel


class WalletAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'money']
    list_filter = ['user_id']


admin.site.register(PurseModel, WalletAdmin)
