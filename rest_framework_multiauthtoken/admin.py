from django.contrib import admin

from .models import Token


class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'name', 'created')
    fields = ('user', 'name')
    ordering = ('-created',)


admin.site.register(Token, TokenAdmin)
