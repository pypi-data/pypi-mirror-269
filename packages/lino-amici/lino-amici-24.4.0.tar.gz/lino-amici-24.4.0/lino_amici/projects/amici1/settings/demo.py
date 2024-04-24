# import os ; print "20161219 %s (pid:%s)" % (__name__, os.getpid())

import datetime
from lino.core.auth.utils import activate_social_auth_testing
from ..settings import *


class Site(Site):
    is_demo_site = True
    the_demo_date = datetime.date(2019, 12, 16)
    languages = "en de fr"

    # is_demo_site = False

    # default_ui = 'lino.modlib.extjs'
    # default_ui = 'lino.modlib.bootstrap3'
    # default_user = 'anonymous'

    def get_plugin_configs(self):
        for i in super().get_plugin_configs():
            yield i
        # yield 'addresses', 'partner_model', 'contacts.Person'
        yield 'users', 'third_party_authentication', True


activate_social_auth_testing(globals(),
                             google=False,
                             github=False,
                             wikimedia=False)

SITE = Site(globals())
# print "20161219 b"
DEBUG = True

# the following line should not be active in a checked-in version
# DATABASES['default']['NAME'] = ':memory:'
