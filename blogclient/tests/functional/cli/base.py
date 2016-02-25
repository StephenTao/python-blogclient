# Copyright (c) 2014 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os

from tempest import config
from tempest_lib.cli import base

CONF = config.CONF


class BlogCLIAuth(base.ClientTestBase):

    _blog_url = None

    def _get_admin_clients(self):
        clients = base.CLIClient(
            username=CONF.identity.admin_username,
            password=CONF.identity.admin_password,
            tenant_name=CONF.identity.admin_tenant_name,
            uri=CONF.identity.uri,
            cli_dir='/usr/local/bin')

        return clients

    def _get_clients(self):
        return self._get_admin_clients()

    def blog(self, action, flags='', params='', fail_ok=False):
        """Executes Blog command."""
        blog_url_op = "--os-blog-url %s" % self._blog_url

        if 'WITHOUT_AUTH' in os.environ:
            return base.execute(
                'blog %s' % blog_url_op, action, flags, params,
                fail_ok, merge_stderr=False, cli_dir='')
        else:
            return self.clients.cmd_with_auth(
                'blog %s' % blog_url_op, action, flags, params,
                fail_ok)


class BlogCLIAltAuth(base.ClientTestBase):

    _blog_url = None

    def _get_alt_clients(self):
        clients = base.CLIClient(
            username=CONF.identity.alt_username,
            password=CONF.identity.alt_password,
            tenant_name=CONF.identity.alt_tenant_name,
            uri=CONF.identity.uri,
            cli_dir='/usr/local/bin')

        return clients

    def _get_clients(self):
        return self._get_alt_clients()

    def blog_alt(self, action, flags='', params='', mode='alt_user'):
        """Executes Blog command for alt_user from alt_tenant."""
        blog_url_op = "--os-blog-url %s" % self._blog_url

        return self.clients.cmd_with_auth(
            'blog %s' % blog_url_op, action, flags, params)
