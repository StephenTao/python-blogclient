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
import time

from tempest_lib import exceptions

from bloglient.tests.functional.cli import base


BLOG_URL = "http://localhost:8989/v1"


class BlogClientTestBase(base.BlogCLIAuth, base.BlogCLIAltAuth):

    _blog_url = BLOG_URL

    @classmethod
    def setUpClass(cls):
        super(BlogClientTestBase, cls).setUpClass()

        cls.wb_def = os.path.relpath(
            'functionaltests/resources/v2/wb_v2.yaml', os.getcwd())

    def setUp(self):
        super(BlogClientTestBase, self).setUp()

    def get_value_of_field(self, obj, field):
        return [o['Value'] for o in obj
                if o['Field'] == "{0}".format(field)][0]

    def get_item_info(self, get_from, get_by, value):
        return [i for i in get_from if i[get_by] == value][0]

    def blog_admin(self, cmd, params=""):
        self.clients = self._get_admin_clients()
        return self.parser.listing(self.mistral(
            '{0}'.format(cmd), params='{0}'.format(params)))

    def blog_alt_user(self, cmd, params=""):
        self.clients = self._get_alt_clients()
        return self.parser.listing(self.mistral_alt(
            '{0}'.format(cmd), params='{0}'.format(params)))

    def blog_cli(self, admin, cmd, params):
        if admin:
            return self.blog_admin(cmd, params)
        else:
            return self.blog_alt_user(cmd, params)

    def blog_create(self, wb_def, admin=True):
        wb = self.blog_cli(
            admin,
            'blog-create',
            params='{0}'.format(wb_def))
        wb_name = self.get_value_of_field(wb, "Name")
        self.addCleanup(self.blog_cli,
                        admin,
                        'blog-delete',
                        params=wb_name)
        self.addCleanup(self.blog_cli,
                        admin,
                        'blog-delete',
                        params='wb.wf1')

        return wb
