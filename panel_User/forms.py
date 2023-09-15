from django import forms
from account_module.models import User
from django.core.exceptions import ValidationError
from django.core import validators


class edit_panel_User_ModelForm(forms.ModelForm):
    class Meta:
        model = User

        fields = ['first_name', 'last_name', 'phone_number', 'address', 'avatar', 'about_user']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'phone_number': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'about_user': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
            })
        }

        labels = {
            'first_name': 'نام شما',
            'last_name': ' نام خانوادگی شما  ',
            'phone_number': 'شماره تماس  شما',
            'address': 'آدرس  شما',
            'avatar': 'عکس پروفایل شما ',
        }

        error_messages = {
            'full_name': {
                'required': 'نام و نام خانوادگی اجباری می باشد. لطفا وارد کنید'
            }
        }


class change_pass_ModelForm(forms.Form):
    current_pass = forms.CharField(
        label='کلمه عبور فعلی',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        validators=(
            validators.MaxLengthValidator(100),
        )
    )
    error_messages = {
        'password': {
            'required': 'نام و نام خانوادگی اجباری می باشد. لطفا وارد کنید'
        }
    }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password

        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')
