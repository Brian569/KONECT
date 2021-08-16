from django import forms
from django.db.models import fields
from .models import Posts, Profile, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Posts
        fields = ['title', 'body', 'image']

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        
    )

    class Meta:
        model = Comment
        fields= ['comment']