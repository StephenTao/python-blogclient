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

from tempest_lib import decorators
from tempest_lib import exceptions

from mistralclient.tests.functional.cli import base
from mistralclient.tests.functional.cli.v1 import base_v1


BLOG_URL = "http://localhost:8989/v1"


class SimpleBlogCLITests(base.BlogCLIAuth):
    """Basic tests, check '-list', '-help' commands."""

    _blog_url = BLOG_URL

    @classmethod
    def setUpClass(cls):
        super(SimpleBlogCLITests, cls).setUpClass()

    def test_blogs_list(self):
        blogs = self.parser.listing(self.blog('blog-list'))
        self.assertTableStruct(
            blogs,
            ['Name', 'Tags', 'Created at', 'Updated at']
        )


class BlogCLITests(base_v1.BlogClientTestBase):
    """Test suite checks commands to work with blogs."""

    @classmethod
    def setUpClass(cls):
        super(BlogCLITests, cls).setUpClass()

    def test_blog_create_delete(self):
        wb = self.blog_admin(
            'blog-create', params=self.wb_def)
        wb_name = self.get_value_of_field(wb, "Name")

        self.assertTableStruct(wb, ['Field', 'Value'])

        wbs = self.blog_admin('blog-list')
        self.assertIn(wb_name, [blog['Name'] for blog in wbs])

        wbs = self.blog_admin('blog-list')
        self.assertIn(wb_name, [blog['Name'] for blog in wbs])

        self.blog_admin('blog-delete', params=wb_name)

        wbs = self.blog_admin('blog-list')
        self.assertNotIn(wb_name, [blog['Name'] for blog in wbs])

    def test_blog_update(self):
        wb = self.blog_create(self.wb_def)
        wb_name = self.get_value_of_field(wb, "Name")

        init_update_at = self.get_value_of_field(wb, "Updated at")
        tags = self.get_value_of_field(wb, 'Tags')
        self.assertNotIn('tag', tags)

        wb = self.blog_admin(
            'blog-update', params=self.wb_def)
        update_at = self.get_value_of_field(wb, "Updated at")
        name = self.get_value_of_field(wb, 'Name')
        tags = self.get_value_of_field(wb, 'Tags')

        self.assertEqual(wb_name, name)
        self.assertNotIn('tag', tags)
        self.assertEqual(init_update_at, update_at)

        wb = self.blog_admin(
            'blog-update', params=self.wb_with_tags_def)
        self.assertTableStruct(wb, ['Field', 'Value'])

        update_at = self.get_value_of_field(wb, "Updated at")
        name = self.get_value_of_field(wb, 'Name')
        tags = self.get_value_of_field(wb, 'Tags')

        self.assertEqual(wb_name, name)
        self.assertIn('tag', tags)
        self.assertNotEqual(init_update_at, update_at)

    def test_blog_get(self):
        created = self.blog_create(self.wb_with_tags_def)
        wb_name = self.get_value_of_field(created, "Name")

        fetched = self.mistral_admin('workbook-get', params=wb_name)

        created_wb_name = self.get_value_of_field(created, 'Name')
        fetched_wb_name = self.get_value_of_field(fetched, 'Name')

        self.assertEqual(created_wb_name, fetched_wb_name)

        created_wb_tag = self.get_value_of_field(created, 'Tags')
        fetched_wb_tag = self.get_value_of_field(fetched, 'Tags')

        self.assertEqual(created_wb_tag, fetched_wb_tag)

    def test_blog_get_definition(self):
        wb = self.workbook_create(self.wb_def)
        wb_name = self.get_value_of_field(wb, "Name")

        definition = self.blog_admin(
            'blog-get-definition', params=wb_name)
        self.assertNotIn('404 Not Found', definition)


class NegativeCLITests(base_v2.MistralClientTestBase):
    """This class contains negative tests."""

    def test_wb_list_extra_param(self):
        self.assertRaises(exceptions.CommandFailed,
                          self.blog_admin,
                          'blog-list',
                          params='param')

    def test_wb_get_unexist_wb(self):
        self.assertRaises(exceptions.CommandFailed,
                          self.blog_admin,
                          'blog-get',
                          params='wb')

    def test_wb_get_without_param(self):
        self.assertRaises(exceptions.CommandFailed,
                          self.blog_admin,
                          'blog-get')

    def test_wb_create_same_name(self):
        self.blog_create(self.wb_def)
        self.assertRaises(exceptions.CommandFailed,
                          self.blog_create,
                          self.wb_def)

    def test_wb_create_with_wrong_path_to_definition(self):
        self.assertRaises(exceptions.CommandFailed,
                          self.blog_admin,
                          'blog_create',
                          'wb')

    def test_wb_delete_unexist_wb(self):
        self.assertRaises(exceptions.CommandFailed,
                          self.blog_admin,
                          'blog-delete',
                          params='wb')

    def test_wb_update_wrong_path_to_def(self):
        self.assertRaises(exceptions.CommandFailed,
                          self.blog_admin,
                          'blog-update',
                          params='wb')

    def test_wb_update_nonexistant_wb(self):
        self.assertRaises(exceptions.CommandFailed,
                          self.blog_admin,
                          'blog-update',
                          params=self.wb_with_tags_def)

    def test_wb_create_empty_def(self):
        self.create_file('empty')
        self.assertRaises(exceptions.CommandFailed,
                          self.blog_admin,
                          'blog-create',
                          params='empty')

    def test_wb_update_empty_def(self):
        self.create_file('empty')
        self.assertRaises(exceptions.CommandFailed,
                          self.blog_admin,
                          'blog-update',
                          params='empty')

    def test_wb_get_definition_unexist_wb(self):
        self.assertRaises(exceptions.CommandFailed,
                          self.blog_admin,
                          'blog-get-definition',
                          params='wb')

    def test_wb_create_invalid_def(self):
        self.assertRaises(exceptions.CommandFailed,
                          self.blog_admin,
                          'blog-create',
                          params=self.wf_def)

    def test_wb_update_invalid_def(self):
        self.assertRaises(exceptions.CommandFailed,
                          self.blog_admin,
                          'blog-update',
                          params=self.wf_def)

    def test_wb_update_without_def(self):
        self.assertRaises(exceptions.CommandFailed,
                          self.blog_admin,
                          'blog-update')