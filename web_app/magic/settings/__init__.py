from magic.settings.django import *

# wrapped in try except so import don't grey out in editor :-)
# or accidentally removed with an import optimization
try:
    from magic.settings.local_settings import *
except ImportError:
    raise