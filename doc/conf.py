from urllib.request import urlopen

from constantdict import __version__

_conf_url = \
    "https://raw.githubusercontent.com/inducer/sphinxconfig/main/sphinxconfig.py"
with urlopen(_conf_url) as _inf:
    exec(compile(_inf.read(), _conf_url, "exec"), globals())

old_linkcode_resolve = linkcode_resolve  # noqa: F821 (linkcode_resolve comes from the URL above)


def linkcode_resolve(*args, **kwargs):
    linkcode_url = "https://github.com/matthiasdiener/constantdict/blob/main/{filepath}#L{linestart}-L{linestop}"
    return old_linkcode_resolve(*args, **kwargs, linkcode_url=linkcode_url)


project = "constantdict"
copyright = "2024, University of Illinois Board of Trustees"
author = "Constantdict contributors"
version = __version__
release = __version__

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pyrsistent": ("https://pyrsistent.readthedocs.io/en/latest/", None),
    "immutabledict": ("https://immutabledict.corenting.fr/", None),
}
