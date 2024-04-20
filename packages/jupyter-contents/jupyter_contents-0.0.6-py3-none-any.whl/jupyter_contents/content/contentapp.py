import warnings

from datalayer.application import NoStart

from ..application_base import JupyterContentBaseApp


class ContentListApp(JupyterContentBaseApp):
    """An application to list the content."""

    description = """
      An application to list the content.
    """

    def initialize(self, *args, **kwargs):
        """Initialize the app."""
        super().initialize(*args, **kwargs)

    def start(self):
        """Start the app."""
        if len(self.extra_args) > 1:  # pragma: no cover
            warnings.warn("Too many arguments were provided for Content list.")
            self.exit(1)
        self.log.info("ContentListApp %s %s %s", self.base_url, self.base_ws_url, self.version)


class ContentApp(JupyterContentBaseApp):
    """A Router application."""

    description = """
      The JupyterContent application for the Router.
    """

    subcommands = {}
    subcommands["list"] = (
        ContentListApp,
        ContentListApp.description.splitlines()[0],
    )

    def start(self):
        try:
            super().start()
            self.log.error(f"One of `{'`, `'.join(ContentApp.subcommands.keys())}` must be specified.")
            self.exit(1)
        except NoStart:
            pass
        self.exit(0)
