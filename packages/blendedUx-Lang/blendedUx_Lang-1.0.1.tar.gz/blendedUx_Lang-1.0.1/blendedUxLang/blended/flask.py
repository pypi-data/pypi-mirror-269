from __future__ import absolute_import
from flask import *
from blendedUxLang.blended.jinjaenv import BlendedEnvironment


class Environment(BlendedEnvironment):
    """ The code here is identical to Flask's subclass of Jinja's
    Environment class, except it extends Blended's own Jinja
    Environment, which adds new tags, functions and parsing behavior.
    """

    def __init__(self, app, **options):
        if 'loader' not in options:
            options['loader'] = app.create_global_jinja_loader()
        BlendedEnvironment.__init__(self, **options)
        self.app = app


class BlendedFlask(Flask):

    def create_jinja_environment(self):
        """ This is the method inside Flask that binds the Jinja
        Environment to the Flask app. Because we use a different
        implementation of Environment, we have to override this
        method to make Blended available inside Flask.
        """
        options = dict(self.jinja_options)
        if 'autoescape' not in options:
            options['autoescape'] = self.select_jinja_autoescape
        rv = Environment(self, **options)
        rv.globals.update(
            url_for=url_for,
            get_flashed_messages=get_flashed_messages,
            config=self.config,
            # request, session and g are normally added with the
            # context processor for efficiency reasons but for imported
            # templates we also want the proxies in there.
            request=request,
            session=session,
            g=g
        )
        rv.filters['tojson'] = json.tojson_filter
        return rv

Flask = BlendedFlask
