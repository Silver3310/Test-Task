from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views import View
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Subscription, Post


class HomePageView(TemplateView):
    """
    Home page view with links to other views
    """

    template_name = "blog/index.html"


class BloggersListView(ListView):
    """
    Bloggers view lists all the bloggers to subscribe/unsubscribe to them
    """

    model = get_user_model()
    template_name = 'blog/bloggers.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscriptions'] = Subscription.all_bloggers_of(self.request.user)
        return context


class SubscribeView(View):
    """
    Subscribe view handles the subscription/cancelling a subscription
    """

    def post(self, request, **kwargs):
        potential_sub = Subscription.objects.filter(
            user=request.user,
            blog_id=kwargs['blogger_id']
        )
        if potential_sub.exists():
            # delete the current subscription
            potential_sub.delete()
        else:
            # create a new subscription
            Subscription(
                user=request.user,
                blog_id=kwargs['blogger_id']
            ).save()

        return HttpResponseRedirect(reverse('bloggers'))


class NewsFeedListView(ListView):
    """
    News feed view shows posts from blogs a user subscribed to
    """

    template_name = 'blog/newsfeed.html'
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        blogs_list = Subscription.all_bloggers_of(self.request.user)
        queryset = Post.objects.filter(blog__in=blogs_list).order_by('-timestamp')
        return queryset
