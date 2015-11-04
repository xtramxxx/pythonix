# coding=utf-8
from __future__ import unicode_literals

from django import template
from django.template.loader import render_to_string

__author__ = 'Jeka'

register = template.Library()


def lite_include(tml, **kwargs):
    return render_to_string(tml, kwargs)

register.simple_tag(lite_include)