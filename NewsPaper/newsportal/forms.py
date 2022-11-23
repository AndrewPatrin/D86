from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    #request = None
    class Meta:
        model = Post
        fields = [
            'post_title',
            'post_text',
            'category',
            #'author',
        ]
