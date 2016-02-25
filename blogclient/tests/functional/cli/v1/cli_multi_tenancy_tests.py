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

from tempest_lib import exceptions

from blogclient.tests.functional.cli.v1 import base_v1


class StandardItemsAvailabilityCLITests(base_v1.BlogClientTestBase):

    def test_std_blogs_availability(self):
        wfs = self.blog_admin("blog-list")

        self.assertTableStruct(
            wfs,
            ["Name", "Tags", "Input", "Created at", "Updated at"]
        )
        self.assertIn("std.create_instance",
                      [blog["Name"] for blog in wfs])

        wfs = self.blog_alt_user("blog-list")

        self.assertTableStruct(
            wfs,
            ["Name", "Tags", "Input", "Created at", "Updated at"]
        )
        self.assertIn("std.create_instance",
                      [blog["Name"] for blog in wfs])


class BlogIsolationCLITests(base_v1.BlogClientTestBase):

    def test_blog_name_uniqueness(self):
        self.blog_create(self.wb_def)

        self.assertRaises(
            exceptions.CommandFailed,
            self.blog_admin,
            "blog-create",
            params="{0}".format(self.wb_def)
        )

        self.blog_create(self.wb_def, admin=False)

        self.assertRaises(
            exceptions.CommandFailed,
            self.blog_alt_user,
            "blog-create",
            params="{0}".format(self.wb_def)
        )

    def test_wb_isolation(self):
        wb = self.blog_create(self.wb_def)
        wb_name = self.get_value_of_field(wb, "Name")
        wbs = self.blog_admin("blog-list")

        self.assertIn(wb_name, [w["Name"] for w in wbs])

        alt_wbs = self.blog_alt_user("blog-list")

        self.assertNotIn(wb_name, [w["Name"] for w in alt_wbs])

    def test_get_wb_from_another_tenant(self):
        wb = self.blog_create(self.wb_def)
        name = self.get_value_of_field(wb, "Name")

        self.assertRaises(
            exceptions.CommandFailed,
            self.blog_alt_user,
            "blog-get",
            params=name
        )

    def test_delete_wb_from_another_tenant(self):
        wb = self.blog_create(self.wb_def)
        name = self.get_value_of_field(wb, "Name")

        self.assertRaises(
            exceptions.CommandFailed,
            self.blog_alt_user,
            "blog-delete",
            params=name
        )
