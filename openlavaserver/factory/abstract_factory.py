import abc
import six
import re
import collections

from openlavaserver.common import printError, printWarning

__all__ = ('BaseController',)

@six.add_metaclass(abc.ABCMeta)
class BaseController(object):
    
    @abc.abstractmethod
    def get_shell_command_dict(self, command):
        """
        Collect (common) openlava command info into a dict.
        It only works with the Title-Item type informations.
        """
        return None
    
    @abc.abstractmethod
    def get_openlava_command_dict(self, command):
        """
        Collect (common) openlava command info into a dict.
        It only works with the Title-Item type informations.
        """
        return None


    def convert_shell_stream_to_list(self, lines=None, command=None):
        parse_dict = collections.OrderedDict()
        for index, value in enumerate(lines):
            line = value.strip()
            parse_dict[index] = line
        
        return parse_dict


    def convert_openlava_stream_to_dict(self, lines=None, command=None):
        parse_dict = collections.OrderedDict()
        key_list = []
        for i in range(len(lines)):
            line = lines[i].strip()

            # Some speciall preprocess.
            if re.search('lsload', command):
                line = re.sub(r'\*', ' ', line)

            if i == 0:
                key_list = line.split()
                for key in key_list:
                    parse_dict[key] = []
            else:
                command_info = line.split()
                if len(command_info) < len(key_list):
                    printWarning('Warning: (get_openlava_command_dict) : For command "' + str(command) + '", below info line is incomplate/unexpected.')
                    printWarning('           ' + str(line))

                for j in range(len(key_list)):
                    key = key_list[j]
                    if j < len(command_info):
                        value = command_info[j]
                    else:
                        value = ''
                    parse_dict[key].append(value)

        return(parse_dict)
    