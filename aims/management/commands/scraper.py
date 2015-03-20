__author__ = 'niko'
import os
from datetime import datetime
from subprocess import call
# Django specific
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    option_list = BaseCommand.option_list
    counter = 0

    def handle(self, *args, **options):
        cmd_dir = os.path.dirname(os.path.realpath(__file__))
        url = args[0]
        # path = datetime.now().isoformat() + ".png"
        if len(args) == 2:
            path = args[1]
        else:
            path = datetime.now().isoformat() + ".pdf"
        command_array = ['phantomjs', cmd_dir+'/poster.js', url, path]
        if path.endswith("pdf"):
            command_array.append("A4")
        # call(['phantomjs', cmd_dir+'/ras.js', url, path])
        call(command_array)
