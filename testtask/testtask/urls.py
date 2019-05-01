from django.contrib import admin
from django.urls import path, include
from .settings.security import ADMIN_URL

urlpatterns = [
    path(
        ADMIN_URL,
        admin.site.urls
    ),
    path(
        '',
        include('blog.urls')
    )
]
