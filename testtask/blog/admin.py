from django.contrib import admin

from .models import Blog, Subscription, Post, ReadPosts


admin.site.register(Blog)
admin.site.register(Subscription)
admin.site.register(Post)
admin.site.register(ReadPosts)
