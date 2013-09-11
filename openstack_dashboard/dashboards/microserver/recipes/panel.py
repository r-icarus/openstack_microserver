from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.microserver import dashboard


class Recipes(horizon.Panel):
    name = _("Recipes")
    slug = "recipes"


dashboard.Microserver.register(Recipes)
