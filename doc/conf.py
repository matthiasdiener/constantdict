from urllib.request import urlopen

from constantdict import __version__

_conf_url = \
    "https://raw.githubusercontent.com/inducer/sphinxconfig/main/sphinxconfig.py"
with urlopen(_conf_url) as _inf:
    exec(compile(_inf.read(), _conf_url, "exec"), globals())

project = "constantdict"
copyright = "2024, University of Illinois Board of Trustees"
author = "Constantdict contributors"
version = __version__
release = __version__

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
