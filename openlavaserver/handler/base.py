import abc
import six

__all__ = ('BaseHandler',)

@six.add_metaclass(abc.ABCMeta)
class BaseHandler(object):

    def __init__(self):
        pass

    @abc.abstractmethod
    def set_next_handler(self, base_handler=None):
        return None

    @abc.abstractmethod
    def handler(self, config=None, **kwargs):
        return None