from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class MyAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
    
    # def save_user(self, request, user, form, commit=False):
    #     data = form.cleaned_data
    #     print('\n' + data+ '\n')
    #     user.username = self.generate_unique_username(data['email'])  # username not in use
    #     user.email = data['email']
    #     if 'password1' in data:
    #         user.set_password(data['password1'])
    #     else:
    #         user.set_unusable_password()
    #     self.populate_username(request, user)
    #     if commit:
    #         user.save()
    #     return user


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
