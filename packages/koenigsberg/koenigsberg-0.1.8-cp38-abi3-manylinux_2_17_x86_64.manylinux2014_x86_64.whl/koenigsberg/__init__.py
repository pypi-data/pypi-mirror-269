from .main import Backend

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__)

ba = Backend()


def con():
    ba.do_connect()
    return ba
