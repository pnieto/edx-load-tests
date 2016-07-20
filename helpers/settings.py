import os
import yaml
import logging
from pkg_resources import resource_filename
from pprint import pformat

LOG = logging.getLogger(__file__)

def init(test_module_full_name):
    """
    This initializes the global settings_dict, and loads settings from the
    correct settings file.  To use this module for your load tests, include the
    following two lines in your locustfile.py:

      from helpers import settings
      settings.init(__name__)

    Then, create a settings file: "settings_files/<TEST MODULE NAME>.yml"
    
    Anywhere you need to use the settings data, make sure the settings module
    is imported, then use:

      settings.data['SOMETHING']

    """
    global data

    # Find the correct settings file under the "settings_files" directory of
    # this package.  The name of the settings file corresponds to the
    # name of the directory containing the locustfile. E.g. "lms/locustfile.py"
    # reads settings data from "settings_files/lms.yml".
    test_module_name = test_module_full_name.split('.')[0]
    settings_filename = \
        resource_filename('settings_files', '%s.yml' % test_module_name)
    settings_filename = os.path.abspath(settings_filename)
    LOG.info('using settings file: %s' % settings_filename)

    # load the settings file
    settings_file = open(settings_filename, 'r')
    data = yaml.load(settings_file)
    settings_file.close()
    LOG.info('loaded the following settings:\n%s' % pformat(data))
