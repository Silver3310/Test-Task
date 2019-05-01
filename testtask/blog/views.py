from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views import View
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

from .models import Subscription, Post, ReadPosts, Blog
from .forms import PostForm


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
            # mark all the posts that as unread by that subscription
            posts_list = Post.objects.filter(blog_id=kwargs['blogger_id'])
            ReadPosts.objects.filter(user=request.user, post__in=posts_list).delete()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['read_news'] = ReadPosts.all_read_posts_of(self.request.user)
        return context


class ReadNewsView(View):
    """
    Read news view handles whether to delete or create a new mark
    """

    def post(self, request, **kwargs):
        potential_sub = ReadPosts.objects.filter(
            user=request.user,
            post_id=kwargs['news_id']
        )
        if potential_sub.exists():
            # delete the current mark
            potential_sub.delete()
        else:
            # create a new mark
            ReadPosts(
                user=request.user,
                post_id=kwargs['news_id']
            ).save()

        return HttpResponseRedirect(reverse('news-feed'))


class PostFormView(FormView):
    """
    Post from view is to add a new post through a website interface
    """
    form_class = PostForm
    template_name = 'blog/add_post.html'
    success_url = reverse_lazy('add-post')

    def form_valid(self, form):
        Post.objects.create(
            title=form.cleaned_data['title'],
            text=form.cleaned_data['text'],
            blog=Blog.objects.get(user=self.request.user)
        )
        email(self.request)
        return super().form_valid(form)


class PersonalBlogListView(ListView):
    """
    a list of a user's own posts
    """
    template_name = 'blog/personal_blog.html'
    paginate_by = 100

    def get_queryset(self):
        blog = Blog.objects.get(user=self.request.user)
        queryset = Post.objects.filter(blog=blog).order_by('-timestamp')
        return queryset


def email(request):
    """
    send an email as a notification to other users
    """
    subject = f'New Post from your subscriber {request.user}'
    message = 'link'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = Subscription.all_subscribers_emails(request.user)
    send_mail(subject, message, email_from, recipient_list)
    return HttpResponseRedirect(reverse('index'))
