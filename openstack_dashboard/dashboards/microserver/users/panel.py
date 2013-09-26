from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.microserver import dashboard


class Users(horizon.Panel):
    name = _("Users")
    slug = "users"


dashboard.Microserver.register(Users)
