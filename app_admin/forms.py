# coding: utf-8
from django import forms

from captcha.fields import CaptchaField


class DelClientForm(forms.Form):

    captcha = CaptchaField()