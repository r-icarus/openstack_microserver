from django.utils.translation import ugettext_lazy as _

import horizon


class Microserver(horizon.Dashboard):
    name = _("Microserver")
    slug = "microserver"
    panels = ('hypervisors','recipes', 'configuration', 'logs','users',)  # Add your panels here.
    default_panel = 'hypervisors'  # Specify the slug of the dashboard's default panel.


horizon.register(Microserver)
