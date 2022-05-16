from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version('incognia-python')
except PackageNotFoundError:
    __version__ = 'unknown'

__all__ = ['api',
           'datetime_util',
           'endpoints',
           'exceptions',
           'feedback_events',
           'json_util',
           'models',
           'token_manager',
           'base_request']
