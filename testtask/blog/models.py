from django.db import models
from django.contrib.auth import get_user_model
from django_auto_one_to_one import AutoOneToOneModel


class Blog(AutoOneToOneModel(get_user_model())):
    """
    Blog model

    Attributes:
        user (User): a user that a blog belongs to
    """

    def __str__(self):
        return f'the blog of the user {self.user}'


class Post(models.Model):
    """
    Post model

    Attributes:
        title (str): a post's title
        text (str): a post's text
        timestamp (datetime): the time when a post was created
        blog (Blog): a blog that a post belongs to
    """

    title = models.CharField(
        max_length=100
    )
    text = models.TextField(
        max_length=3000
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Subscription(models.Model):
    """
    Subscription model

    Attributes:
        user (User): a subscriber
        blog (Blog): a blog that a user is subscribed to
    """

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE
    )

    @staticmethod
    def all_bloggers_of(user):
        """
        all bloggers that a user follows
        """
        list_of_blogs = Subscription.objects.filter(user=user)
        return [blog.blog_id for blog in list_of_blogs]

    @staticmethod
    def all_subscribers_emails(user):
        """
        Return emails of a user's subscribers
        """
        blog = Blog.objects.get(user=user)
        list_of_subscriptions = Subscription.objects.filter(blog=blog)
        return [sub.user.email for sub in list_of_subscriptions]


class ReadPosts(models.Model):
    """
    ReadPosts model

    Attributes:
        user (User): a user who has read the post
        post (Post): a post that a user has read
    """

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )

    @staticmethod
    def all_read_posts_of(user):
        """
        all the posts that a user marked as read
        """
        list_of_posts = ReadPosts.objects.filter(user=user)
        return [post.post_id for post in list_of_posts]
