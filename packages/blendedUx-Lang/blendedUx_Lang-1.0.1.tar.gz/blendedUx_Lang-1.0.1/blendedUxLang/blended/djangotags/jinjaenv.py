from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse

from blendedUxLang.blended.jinjaenv import BlendedEnvironment


def environment(**options):
    env = BlendedEnvironment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
