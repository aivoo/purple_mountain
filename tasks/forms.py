from django import forms

from .models import Tutorial


class PostForm(forms.ModelForm):

    class Meta:
        model = Tutorial
        fields = ('title', 'index', 'content',)
