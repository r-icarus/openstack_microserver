from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.microserver import dashboard


class Logs(horizon.Panel):
    name = _("Logs")
    slug = "logs"


dashboard.Microserver.register(Logs)
