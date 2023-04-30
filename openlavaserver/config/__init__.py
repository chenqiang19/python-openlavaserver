
import os
from config.base import Configuration

__all__ = ('CONF', 'configure',)

CONF = Configuration()

def configure(project, setup=True):
    if (setup):
        CONF.setup(project, os.environ.copy())


