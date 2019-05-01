from django.urls import path

from . import views


urlpatterns = [
    path(
        '',
        views.HomePageView.as_view(),
        name='index'
    ),
    path(
        'bloggers/',
        views.BloggersListView.as_view(),
        name='bloggers'
    ),
    path(
        'subscribe/<int:blogger_id>/',
        views.SubscribeView.as_view(),
        name='subscribe'
    )
]
