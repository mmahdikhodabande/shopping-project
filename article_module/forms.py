from django import forms
from article_module.models import Article_comment


class Article_commentModelForm(forms.ModelForm):
    class Meta:
        model = Article_comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'id': 'message'
            })
        }

        labels = {
            'text': 'نظر شما راجب این  مقاله   ',
        }

        error_messages = {
            'text': {
                'required': 'متن نظر شما خالی میباشد '
            }
        }
