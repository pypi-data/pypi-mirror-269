from ._version import __version__

from traitlets import Bool, Unicode

from datalayer.application import DatalayerApp, base_aliases, base_flags


jupyter_contents_aliases = dict(base_aliases)
jupyter_contents_aliases["cloud"] = "JupyterContentBaseApp.cloud"
jupyter_contents_aliases["server-base-url"] = "JupyterContentBaseApp.server_base_url"
jupyter_contents_aliases["server-base-ws-url"] = "JupyterContentBaseApp.server_base_ws_url"
jupyter_contents_aliases["server-token"] = "JupyterContentBaseApp.server_token"

jupyter_contents_flags = dict(base_flags)
jupyter_contents_flags["no-minimize"] = (
    {"JupyterContentBaseApp": {"minimize": False}},
    "Do not minimize a production build.",
)


class JupyterContentBaseApp(DatalayerApp):
    name = "jupyter_contents"

    version = __version__

    aliases = jupyter_contents_aliases

    flags = jupyter_contents_flags

    cloud = Unicode("ovh", config=True, help="")

    minimize = Bool(True, config=True, help="")

    server_base_url = Unicode("http://localhost:8888", config=True, help="")

    server_base_ws_url = Unicode("ws://localhost:8888", config=True, help="")

    server_token = Unicode("60c1661cc408f978c309d04157af55c9588ff9557c9380e4fb50785750703da6", config=True, help="")

    router_url = Unicode("http://jupyter-router-api-svc:2001/api/routes", config=True, help="")

    router_token = Unicode("test", config=True, help="")

    lang = Unicode("python", config=True, help="")

    kernel_id = Unicode(None, allow_none=True, config=True, help="")
