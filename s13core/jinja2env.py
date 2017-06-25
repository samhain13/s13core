from django.contrib import messages
from django.urls import reverse
from jinja2 import Environment

import s13core.helpers as helpers


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'get_messages': messages.get_messages,
        'h': helpers,
        'reverse': reverse,
        'dir': dir
    })
    return env
