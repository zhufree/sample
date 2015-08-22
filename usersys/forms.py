# -*-coding:utf-8-*-
from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class TextInputWidget(forms.TextInput):
    class Media:
        css = {
            'all': ('pretty.css',)
        }
        js = ('animations.js', 'actions.js')


class RegistrationForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=30)
    email = forms.EmailField(label='注册邮箱', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password2(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 != password2:
                raise forms.ValidationError('两次输入密码不匹配.')
            elif len(password1) < 6:
                raise forms.ValidationError('密码过短,至少6位.')
            else:
                return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\S+$', username):
            raise forms.ValidationError('用户名包含非法字符.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('用户名已存在.')
