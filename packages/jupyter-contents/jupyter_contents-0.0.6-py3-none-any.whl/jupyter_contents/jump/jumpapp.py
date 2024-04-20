import warnings

from datalayer.application import NoStart

from ..application_base import JupyterContentBaseApp


class JumpListApp(JupyterContentBaseApp):
    """An application to list the jump."""

    description = """
      An application to list the jump.
    """

    def initialize(self, *args, **kwargs):
        """Initialize the app."""
        super().initialize(*args, **kwargs)

    def start(self):
        """Start the app."""
        if len(self.extra_args) > 1:  # pragma: no cover
            warnings.warn("Too many arguments were provided for Jump list.")
            self.exit(1)
        self.log.info("JumpListApp %s %s %s", self.base_url, self.base_ws_url, self.version)


class JumpApp(JupyterContentBaseApp):
    """A Jump application."""

    description = """
      The JupyterContent application for the Jump.
    """

    subcommands = {}
    subcommands["list"] = (
        JumpListApp,
        JumpListApp.description.splitlines()[0],
    )

    def start(self):
        try:
            super().start()
            self.log.error(f"One of `{'`, `'.join(JumpApp.subcommands.keys())}` must be specified.")
            self.exit(1)
        except NoStart:
            pass
        self.exit(0)
