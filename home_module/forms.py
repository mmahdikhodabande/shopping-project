from django import forms
from .models import add_email_for_off


class Add_email_off_ModelForm(forms.ModelForm):
    class Meta:
        model = add_email_for_off
        fields = ('email',)
        widgets = {
            'email': forms.TextInput(attrs={
                'type': 'email',
                'placeholder': 'آدرس ایمیل  . . .'
            }),
        }
        labels = {
            'email': ''
        }

        error_messages = {
            'email': {
                'required': 'ایمیل شما اضافه نشده است !!'
            }
        }

        # class Add_email_off_ModelForm(forms.ModelForm):
#     class Meta:
#         model = add_email_for_off
#         fields = ['email']
#         widgets = {
#             'email': forms.TextInput(),
#         }
#         labels = {
#             'email': 'ایمیل شما'
#         }
#
#         error_messages = {
#             'email': {
#                 'required': 'ایمیل شما اضافه نشده است !!'
#             }
#         }
