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
    ),
    path(
        'news-feed/',
        views.NewsFeedListView.as_view(),
        name='news-feed'
    ),
    path(
        'read-news/<int:news_id>/',
        views.ReadNewsView.as_view(),
        name='read-news'
    ),
    path(
        'add-post/',
        views.PostFormView.as_view(),
        name='add-post'
    ),
    path(
        'personal-blog/',
        views.PersonalBlogListView.as_view(),
        name='personal-blog'
    ),
    path(
        'detail-info/<int:pk>/',
        views.PostDetailView.as_view(),
        name='post-detail'
    )
]
