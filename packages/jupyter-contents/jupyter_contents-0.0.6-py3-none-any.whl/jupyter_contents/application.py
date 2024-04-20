import sys
import warnings
from pathlib import Path

from datalayer.application import NoStart

from ._version import __version__
from .application_base import JupyterContentBaseApp
from .content.contentapp import ContentApp
from .jump.jumpapp import JumpApp


HERE = Path(__file__).parent


class ConfigExportApp(JupyterContentBaseApp):
    """An application to export the configuration."""

    description = """
      An application to export the configuration
    """

    def initialize(self, *args, **kwargs):
        """Initialize the app."""
        super().initialize(*args, **kwargs)

    def start(self):
        """Start the app."""
        if len(self.extra_args) > 1:  # pragma: no cover
            warnings.warn("Too many arguments were provided for workspace export.")
            self.exit(1)
        self.log.info("ConfigApp %s", self.version)


class ConfigApp(JupyterContentBaseApp):
    """A config app."""

    description = """
    Manage the configuration.
    """

    subcommands = {}
    subcommands["export"] = (
        ConfigExportApp,
        ConfigExportApp.description.splitlines()[0],
    )

    def start(self):
        try:
            super().start()
            self.log.error(f"One of `{'`, `'.join(ConfigApp.subcommands.keys())}` must be specified.")
            self.exit(1)
        except NoStart:
            pass
        self.exit(0)


class ShellApp(JupyterContentBaseApp):
    """A shell application."""

    description = """
      Run predefined scripts.
    """

    def start(self):
        super().start()
        args = sys.argv
        self.log.info(args)


class JupyterContentApp(JupyterContentBaseApp):
    description = """
      The JupyterContent application.
    """

    subcommands = {
        "config": (ConfigApp, ConfigApp.description.splitlines()[0]),
        "content": (ContentApp, ContentApp.description.splitlines()[0]),
        "jump": (JumpApp, JumpApp.description.splitlines()[0]),
        "sh": (ShellApp, ShellApp.description.splitlines()[0]),
    }

    def initialize(self, argv=None):
        """Subclass because the ExtensionApp.initialize() method does not take arguments."""
        super().initialize()

    def start(self):
        super(JupyterContentApp, self).start()
        self.log.info("JupyterContent - Version %s - Cloud %s ", self.version, self.cloud)


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

main = launch_new_instance = JupyterContentApp.launch_instance

if __name__ == "__main__":
    main()
