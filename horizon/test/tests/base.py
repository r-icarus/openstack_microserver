# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Openstack, LLC
# Copyright 2012 Nebula, Inc.
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

from django.conf import settings  # noqa
from django.contrib.auth.models import User  # noqa
from django.core import urlresolvers
from django.utils.importlib import import_module  # noqa

import horizon
from horizon import base
from horizon import conf
from horizon.test import helpers as test
from horizon.test.test_dashboards.cats.dashboard import Cats  # noqa
from horizon.test.test_dashboards.cats.kittens.panel import Kittens  # noqa
from horizon.test.test_dashboards.cats.tigers.panel import Tigers  # noqa
from horizon.test.test_dashboards.dogs.dashboard import Dogs  # noqa
from horizon.test.test_dashboards.dogs.puppies.panel import Puppies  # noqa


class MyDash(horizon.Dashboard):
    name = "My Dashboard"
    slug = "mydash"
    default_panel = "myslug"


class MyPanel(horizon.Panel):
    name = "My Panel"
    slug = "myslug"
    urls = 'horizon.test.test_dashboards.cats.kittens.urls'


class AdminPanel(horizon.Panel):
    name = "Admin Panel"
    slug = "admin_panel"
    permissions = ("horizon.test",)
    urls = 'horizon.test.test_dashboards.cats.kittens.urls'


class BaseHorizonTests(test.TestCase):

    def setUp(self):
        super(BaseHorizonTests, self).setUp()
        # Adjust our horizon config and register our custom dashboards/panels.
        self.old_default_dash = settings.HORIZON_CONFIG['default_dashboard']
        settings.HORIZON_CONFIG['default_dashboard'] = 'cats'
        self.old_dashboards = settings.HORIZON_CONFIG['dashboards']
        settings.HORIZON_CONFIG['dashboards'] = ('cats', 'dogs')
        base.Horizon.register(Cats)
        base.Horizon.register(Dogs)
        Cats.register(Kittens)
        Cats.register(Tigers)
        Dogs.register(Puppies)
        # Trigger discovery, registration, and URLconf generation if it
        # hasn't happened yet.
        base.Horizon._urls()
        # Store our original dashboards
        self._discovered_dashboards = base.Horizon._registry.keys()
        # Gather up and store our original panels for each dashboard
        self._discovered_panels = {}
        for dash in self._discovered_dashboards:
            panels = base.Horizon._registry[dash]._registry.keys()
            self._discovered_panels[dash] = panels

    def tearDown(self):
        super(BaseHorizonTests, self).tearDown()
        # Restore our settings
        settings.HORIZON_CONFIG['default_dashboard'] = self.old_default_dash
        settings.HORIZON_CONFIG['dashboards'] = self.old_dashboards
        # Destroy our singleton and re-create it.
        base.HorizonSite._instance = None
        del base.Horizon
        base.Horizon = base.HorizonSite()
        # Reload the convenience references to Horizon stored in __init__
        reload(import_module("horizon"))
        # Re-register our original dashboards and panels.
        # This is necessary because autodiscovery only works on the first
        # import, and calling reload introduces innumerable additional
        # problems. Manual re-registration is the only good way for testing.
        self._discovered_dashboards.remove(Cats)
        self._discovered_dashboards.remove(Dogs)
        for dash in self._discovered_dashboards:
            base.Horizon.register(dash)
            for panel in self._discovered_panels[dash]:
                dash.register(panel)

    def _reload_urls(self):
        '''
        Clears out the URL caches, reloads the root urls module, and
        re-triggers the autodiscovery mechanism for Horizon. Allows URLs
        to be re-calculated after registering new dashboards. Useful
        only for testing and should never be used on a live site.
        '''
        urlresolvers.clear_url_caches()
        reload(import_module(settings.ROOT_URLCONF))
        base.Horizon._urls()


class HorizonTests(BaseHorizonTests):

    def test_registry(self):
        """ Verify registration and autodiscovery work correctly.

        Please note that this implicitly tests that autodiscovery works
        by virtue of the fact that the dashboards listed in
        ``settings.INSTALLED_APPS`` are loaded from the start.
        """
        # Registration
        self.assertEqual(len(base.Horizon._registry), 2)
        horizon.register(MyDash)
        self.assertEqual(len(base.Horizon._registry), 3)
        with self.assertRaises(ValueError):
            horizon.register(MyPanel)
        with self.assertRaises(ValueError):
            horizon.register("MyPanel")

        # Retrieval
        my_dash_instance_by_name = horizon.get_dashboard("mydash")
        self.assertTrue(isinstance(my_dash_instance_by_name, MyDash))
        my_dash_instance_by_class = horizon.get_dashboard(MyDash)
        self.assertEqual(my_dash_instance_by_name, my_dash_instance_by_class)
        with self.assertRaises(base.NotRegistered):
            horizon.get_dashboard("fake")
        self.assertQuerysetEqual(horizon.get_dashboards(),
                                 ['<Dashboard: cats>',
                                  '<Dashboard: dogs>',
                                  '<Dashboard: mydash>'])

        # Removal
        self.assertEqual(len(base.Horizon._registry), 3)
        horizon.unregister(MyDash)
        self.assertEqual(len(base.Horizon._registry), 2)
        with self.assertRaises(base.NotRegistered):
            horizon.get_dashboard(MyDash)

    def test_site(self):
        self.assertEqual(unicode(base.Horizon), "Horizon")
        self.assertEqual(repr(base.Horizon), "<Site: horizon>")
        dash = base.Horizon.get_dashboard('cats')
        self.assertEqual(base.Horizon.get_default_dashboard(), dash)
        test_user = User()
        self.assertEqual(base.Horizon.get_user_home(test_user),
                         dash.get_absolute_url())

    def test_dashboard(self):
        cats = horizon.get_dashboard("cats")
        self.assertEqual(cats._registered_with, base.Horizon)
        self.assertQuerysetEqual(cats.get_panels(),
                                 ['<Panel: kittens>',
                                  '<Panel: tigers>'])
        self.assertEqual(cats.get_absolute_url(), "/cats/")
        self.assertEqual(cats.name, "Cats")

        # Test registering a module with a dashboard that defines panels
        # as a panel group.
        cats.register(MyPanel)
        self.assertQuerysetEqual(cats.get_panel_groups()['other'],
                                 ['<Panel: myslug>'])

        # Test that panels defined as a tuple still return a PanelGroup
        dogs = horizon.get_dashboard("dogs")
        self.assertQuerysetEqual(dogs.get_panel_groups().values(),
                                 ['<PanelGroup: default>'])

        # Test registering a module with a dashboard that defines panels
        # as a tuple.
        dogs = horizon.get_dashboard("dogs")
        dogs.register(MyPanel)
        self.assertQuerysetEqual(dogs.get_panels(),
                                 ['<Panel: puppies>',
                                  '<Panel: myslug>'])

    def test_panels(self):
        cats = horizon.get_dashboard("cats")
        tigers = cats.get_panel("tigers")
        self.assertEqual(tigers._registered_with, cats)
        self.assertEqual(tigers.get_absolute_url(), "/cats/tigers/")

    def test_index_url_name(self):
        cats = horizon.get_dashboard("cats")
        tigers = cats.get_panel("tigers")
        tigers.index_url_name = "does_not_exist"
        with self.assertRaises(urlresolvers.NoReverseMatch):
            tigers.get_absolute_url()
        tigers.index_url_name = "index"
        self.assertEqual(tigers.get_absolute_url(), "/cats/tigers/")

    def test_lazy_urls(self):
        urlpatterns = horizon.urls[0]
        self.assertTrue(isinstance(urlpatterns, base.LazyURLPattern))
        # The following two methods simply should not raise any exceptions
        iter(urlpatterns)
        reversed(urlpatterns)

    def test_horizon_test_isolation_1(self):
        """ Isolation Test Part 1: sets a value. """
        cats = horizon.get_dashboard("cats")
        cats.evil = True

    def test_horizon_test_isolation_2(self):
        """ Isolation Test Part 2: The value set in part 1 should be gone. """
        cats = horizon.get_dashboard("cats")
        self.assertFalse(hasattr(cats, "evil"))

    def test_public(self):
        dogs = horizon.get_dashboard("dogs")
        # Known to have no restrictions on it other than being logged in.
        puppies = dogs.get_panel("puppies")
        url = puppies.get_absolute_url()

        # Get a clean, logged out client instance.
        self.client.logout()

        resp = self.client.get(url)
        redirect_url = "?".join(['http://testserver' + settings.LOGIN_URL,
                                 "next=%s" % url])
        self.assertRedirects(resp, redirect_url)

        # Simulate ajax call
        resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # Response should be HTTP 401 with redirect header
        self.assertEquals(resp.status_code, 401)
        self.assertEquals(resp["X-Horizon-Location"],
                          redirect_url)

    def test_required_permissions(self):
        dash = horizon.get_dashboard("cats")
        panel = dash.get_panel('tigers')

        # Non-admin user
        self.assertQuerysetEqual(self.user.get_all_permissions(), [])

        resp = self.client.get(panel.get_absolute_url())
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get(panel.get_absolute_url(),
                               follow=False,
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 401)

        # Test insufficient permissions for logged-in user
        resp = self.client.get(panel.get_absolute_url(), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "auth/login.html")
        self.assertContains(resp, "Login as different user", 1, 200)

        # Set roles for admin user
        self.set_permissions(permissions=['test'])

        resp = self.client.get(panel.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

        # Test modal form
        resp = self.client.get(panel.get_absolute_url(),
                               follow=False,
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)

    def test_ssl_redirect_by_proxy(self):
        dogs = horizon.get_dashboard("dogs")
        puppies = dogs.get_panel("puppies")
        url = puppies.get_absolute_url()
        redirect_url = "?".join([settings.LOGIN_URL,
                                 "next=%s" % url])

        self.client.logout()
        resp = self.client.get(url)
        self.assertRedirects(resp, redirect_url)

        # Set SSL settings for test server
        settings.SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL',
                                            'https')

        resp = self.client.get(url, HTTP_X_FORWARDED_PROTOCOL="https")
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['location'],
                         'https://testserver:80%s' % redirect_url)

        # Restore settings
        settings.SECURE_PROXY_SSL_HEADER = None


class CustomPanelTests(BaseHorizonTests):

    """ Test customization of dashboards and panels
    using 'customization_module' to HORIZON_CONFIG.
    """

    def setUp(self):
        settings.HORIZON_CONFIG['customization_module'] = \
            'horizon.test.customization.cust_test1'
        # refresh config
        conf.HORIZON_CONFIG._setup()
        super(CustomPanelTests, self).setUp()

    def tearDown(self):
        # Restore dash
        cats = horizon.get_dashboard("cats")
        cats.name = "Cats"
        horizon.register(Dogs)
        self._discovered_dashboards.append(Dogs)
        Dogs.register(Puppies)
        Cats.register(Tigers)
        super(CustomPanelTests, self).tearDown()
        settings.HORIZON_CONFIG.pop('customization_module')
        # refresh config
        conf.HORIZON_CONFIG._setup()

    def test_customize_dashboard(self):
        cats = horizon.get_dashboard("cats")
        self.assertEqual(cats.name, "WildCats")
        self.assertQuerysetEqual(cats.get_panels(),
                                 ['<Panel: kittens>'])
        with self.assertRaises(base.NotRegistered):
            horizon.get_dashboard("dogs")


class CustomPermissionsTests(BaseHorizonTests):

    """ Test customization of permissions on panels
    using 'customization_module' to HORIZON_CONFIG.
    """

    def setUp(self):
        settings.HORIZON_CONFIG['customization_module'] = \
            'horizon.test.customization.cust_test2'
        # refresh config
        conf.HORIZON_CONFIG._setup()
        super(CustomPermissionsTests, self).setUp()

    def tearDown(self):
        # Restore permissions
        dogs = horizon.get_dashboard("dogs")
        puppies = dogs.get_panel("puppies")
        puppies.permissions = tuple([])
        super(CustomPermissionsTests, self).tearDown()
        settings.HORIZON_CONFIG.pop('customization_module')
        # refresh config
        conf.HORIZON_CONFIG._setup()

    def test_customized_permissions(self):
        dogs = horizon.get_dashboard("dogs")
        panel = dogs.get_panel('puppies')

        # Non-admin user
        self.assertQuerysetEqual(self.user.get_all_permissions(), [])

        resp = self.client.get(panel.get_absolute_url())
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get(panel.get_absolute_url(),
                               follow=False,
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 401)

        # Test customized permissions for logged-in user
        resp = self.client.get(panel.get_absolute_url(), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "auth/login.html")
        self.assertContains(resp, "Login as different user", 1, 200)

        # Set roles for admin user
        self.set_permissions(permissions=['test'])

        resp = self.client.get(panel.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

        # Test modal form
        resp = self.client.get(panel.get_absolute_url(),
                               follow=False,
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
