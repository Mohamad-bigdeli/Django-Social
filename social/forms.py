from django import forms
from .models import *

class SearchForm(forms.Form):
    query = forms.CharField()


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['body']

class CreatePostForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    
    class Meta:
        model = Post
        fields = ['caption', 'tags']

