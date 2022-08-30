from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from users.models import Follow


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


class NewUserAdmin(UserAdmin):
    list_filter = ('username', 'email')

admin.site.register(Follow, FollowAdmin)
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)
