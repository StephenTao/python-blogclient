# Copyright 2014 - Mirantis, Inc.
# Copyright 2015 - StackStorm, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import argparse
import logging

from cliff import command
from cliff import show

from blogclient.api.v1 import blogs
from blogclient.commands.v1 import base
from blogclient import exceptions as exc
from blogclient import utils


LOG = logging.getLogger(__name__)


def format(blog=None):
    columns = (
        'Id',
        'Title',
        'Content',
        'Creator',
        'Created Time',
        'Updated Time'
    )

    if blog:
        data = (
            blog.id,
            blog.title,
            blog.content,
            blog.creator,
            blog.created_time,
        )

        if hasattr(blog, 'updated_time'):
            data += (blog.updated_time,)
        else:
            data += (None,)

    else:
        data = (tuple('<none>' for _ in range(len(columns))),)

    return columns, data


class List(base.BlogLister):
    """List all blogs."""

    def _get_format_function(self):
        return format

    def _get_resources(self, parsed_args):
        print blogs.BlogManager(self.app.client).list()
        return blogs.BlogManager(self.app.client).list()


class Get(show.ShowOne):
    """Show specific blog."""

    def get_parser(self, prog_name):
        parser = super(Get, self).get_parser(prog_name)

        parser.add_argument(
            'title',
            help='Blog title'
        )

        return parser

    def take_action(self, parsed_args):
        blog = blogs.BlogManager(self.app.client).get(
            parsed_args.title)
        print blog
        return format(blog)


class Add(show.ShowOne):
    "Create new blog by string json data"

    def get_parser(self, prog_name):
        parser = super(Add, self).get_parser(prog_name)

        parser.add_argument(
            'definition',
            help='Blog definition json'
        )

        return parser

    def take_action(self, parsed_args):
        blog = blogs.BlogManager(self.app.client).add(parsed_args.definition)
        return format(blog)


class Create(show.ShowOne):
    """Create new blog."""

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)

        parser.add_argument(
            'definition',
            type=argparse.FileType('r'),
            help='Blog definition file'
        )

        return parser

    def take_action(self, parsed_args):
        blog = blogs.BlogManager(self.app.client).create(
            parsed_args.definition.read())
        return format(blog)


class Delete(command.Command):
    """Delete blog."""

    def get_parser(self, prog_name):
        parser = super(Delete, self).get_parser(prog_name)

        parser.add_argument('title', nargs='+', help='Title of blog(s).')

        return parser

    def take_action(self, parsed_args):
        wb_mgr = blogs.BlogManager(self.app.client)
        utils.do_action_on_many(
            lambda s: wb_mgr.delete(s),
            parsed_args.title,
            "Request to delete blog %s has been accepted.",
            "Unable to delete the specified blog(s)."
        )


class Update(show.ShowOne):
    """Update blog."""

    def get_parser(self, prog_name):
        parser = super(Update, self).get_parser(prog_name)

        parser.add_argument(
            'definition',
            type=argparse.FileType('r'),
            help='Blog definition file'
        )

        return parser

    def take_action(self, parsed_args):
        blog = blogs.BlogManager(self.app.client).update(
            parsed_args.definition.read())

        return format(blog)


class GetDefinition(command.Command):
    """Show blog definition."""

    def get_parser(self, prog_name):
        parser = super(GetDefinition, self).get_parser(prog_name)

        parser.add_argument('title', help='Blog title')

        return parser

    def take_action(self, parsed_args):
        definition = blogs.BlogManager(self.app.client).get(
            parsed_args.title).definition

        self.app.stdout.write(definition or "\n")


class Validate(show.ShowOne):
    """Validate blog."""

    def get_parser(self, prog_name):
        parser = super(Validate, self).get_parser(prog_name)

        parser.add_argument(
            'definition',
            type=argparse.FileType('r'),
            help='Blog definition file'
        )

        return parser

    def take_action(self, parsed_args):
        result = blogs.BlogManager(self.app.client).validate(
            parsed_args.definition.read())

        if not result.get('valid', None):
            raise exc.BlogClientException(
                result.get('error', 'Unknown exception.'))

        return tuple(), tuple()
