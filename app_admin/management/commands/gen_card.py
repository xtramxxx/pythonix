# coding: utf-8
from django.core.management.base import BaseCommand, CommandError

from app_admin.models import GenCardModel

__author__ = 'tram'

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('info', nargs='+', type=int)

    def handle(self, *args, **options):
        gen_card = GenCardModel()
        gen_card.f_gen_card(options['info'][0], options['info'][1])
        print "Card Created"