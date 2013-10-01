# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013, Big Switch Networks
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from django.core.urlresolvers import reverse  # noqa
from django.utils.translation import ugettext_lazy as _  # noqa

from horizon import exceptions
from horizon import forms

from openstack_dashboard import api
from openstack_dashboard.dashboards.project.routers.extensions.routerrules\
    import forms as rrforms


LOG = logging.getLogger(__name__)


class AddRouterRuleView(forms.ModalFormView):
    form_class = rrforms.AddRouterRule
    template_name = 'project/routers/extensions/routerrules/create.html'
    success_url = 'horizon:project:routers:detail'
    failure_url = 'horizon:project:routers:detail'

    def get_success_url(self):
        return reverse(self.success_url,
                       args=(self.kwargs['router_id'],))

    def get_object(self):
        if not hasattr(self, "_object"):
            try:
                router_id = self.kwargs["router_id"]
                self._object = api.neutron.router_get(self.request,
                                                      router_id)
            except Exception:
                redirect = reverse(self.failure_url, args=[router_id])
                msg = _("Unable to retrieve router.")
                exceptions.handle(self.request, msg, redirect=redirect)
        return self._object

    def get_context_data(self, **kwargs):
        context = super(AddRouterRuleView, self).get_context_data(**kwargs)
        context['router'] = self.get_object()
        return context

    def get_initial(self):
        router = self.get_object()
        # store the router in the request so the rule manager doesn't have
        # to request it again from the API
        self.request.META['router'] = router
        return {"router_id": self.kwargs['router_id'],
                "router_name": router.name}
