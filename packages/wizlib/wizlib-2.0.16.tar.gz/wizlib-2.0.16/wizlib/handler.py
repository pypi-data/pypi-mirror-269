from argparse import Action


class Handler:
    """Base class for handlers"""

    appname = None
    default = ''

    @classmethod
    def option_properties(cls, app):
        """Argparse keyword arguments for this optional arg"""
        return {
            'type': cls.setup(app.name),
            'default': cls.default
        }

    @classmethod
    def setup(cls, name=None):
        """Return a callable that returns an instance of the handler object
        that's referenced by commands. In the default case, an instance of the
        handler class itself that knows the name of the app."""
        class NamedHandler(cls):
            appname = name
        return NamedHandler
