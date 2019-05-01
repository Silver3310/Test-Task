from django.db import models
from django.contrib.auth import get_user_model


class Blog(models.Model):
    """
    Blog model

    Attributes:
        user (User): a user that a blog belongs to
    """

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE
    )

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
        is_subscribed (bool): True if subscribed, False otherwise
    """

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE
    )
    is_subscribed = models.BooleanField


class ReadPosts(models.Model):
    """
    ReadPosts model

    Attributes:
        user (User): a user who has read the post
        post (Post): a post that a user has read
        is_read (bool): True if a user has read the post, False otherwise
    """

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    is_read = models.BooleanField
