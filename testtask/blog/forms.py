from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    field_order = ['title', 'text']

    class Meta:
        model = Post
        fields = ('title', 'text')
