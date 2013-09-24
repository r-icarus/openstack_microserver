from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.microserver import dashboard


class Configuration(horizon.Panel):
    name = _("Configuration")
    slug = "configuration"


dashboard.Microserver.register(Configuration)
