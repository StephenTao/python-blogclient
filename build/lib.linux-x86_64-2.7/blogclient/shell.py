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

"""
Command-line interface to the Blog APIs
"""

import logging
import sys

from blogclient.api import client
import blogclient.commands.v1.blogs
from blogclient.openstack.common import cliutils as c

from cliff import app
from cliff import commandmanager

import argparse

LOG = logging.getLogger(__name__)


class OpenStackHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog, indent_increment=2, max_help_position=32,
                 width=None):
        super(OpenStackHelpFormatter, self).__init__(prog, indent_increment,
                                                     max_help_position, width)

    def start_section(self, heading):
        # Title-case the headings.
        heading = '%s%s' % (heading[0].upper(), heading[1:])
        super(OpenStackHelpFormatter, self).start_section(heading)


class HelpAction(argparse.Action):
    """Custom help action.

    Provide a custom action so the -h and --help options
    to the main app will print a list of the commands.

    The commands are determined by checking the CommandManager
    instance, passed in as the "default" value for the action.

    """
    def __call__(self, parser, namespace, values, option_string=None):
        outputs = []
        max_len = 0
        app = self.default
        parser.print_help(app.stdout)
        app.stdout.write('\nCommands for API v1 :\n')

        for name, ep in sorted(app.command_manager):
            factory = ep.load()
            cmd = factory(self, None)
            one_liner = cmd.get_description().split('\n')[0]
            outputs.append((name, one_liner))
            max_len = max(len(name), max_len)

        for (name, one_liner) in outputs:
            app.stdout.write('  %s  %s\n' % (name.ljust(max_len), one_liner))

        sys.exit(0)


class BlogShell(app.App):

    def __init__(self):
        super(BlogShell, self).__init__(
            description=__doc__.strip(),
            version='0.1',
            command_manager=commandmanager.CommandManager('blog.cli'),
        )

        # Set v1 commands by default
        self._set_shell_commands(self._get_commands_v1())

    def configure_logging(self):
        super(BlogShell, self).configure_logging()
        logging.getLogger('iso8601').setLevel(logging.WARNING)
        if self.options.verbose_level <= 1:
            logging.getLogger('requests').setLevel(logging.WARNING)

    def build_option_parser(self, description, version,
                            argparse_kwargs=None):
        """Return an argparse option parser for this application.

        Subclasses may override this method to extend
        the parser with more global options.

        :param description: full description of the application
        :paramtype description: str
        :param version: version number for the application
        :paramtype version: str
        :param argparse_kwargs: extra keyword argument passed to the
                                ArgumentParser constructor
        :paramtype extra_kwargs: dict
        """
        argparse_kwargs = argparse_kwargs or {}
        parser = argparse.ArgumentParser(
            description=description,
            add_help=False,
            formatter_class=OpenStackHelpFormatter,
            **argparse_kwargs
        )
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s {0}'.format(version),
            help='Show program\'s version number and exit.'
        )
        parser.add_argument(
            '-v', '--verbose',
            action='count',
            dest='verbose_level',
            default=self.DEFAULT_VERBOSE_LEVEL,
            help='Increase verbosity of output. Can be repeated.',
        )
        parser.add_argument(
            '--log-file',
            action='store',
            default=None,
            help='Specify a file to log output. Disabled by default.',
        )
        parser.add_argument(
            '-q', '--quiet',
            action='store_const',
            dest='verbose_level',
            const=0,
            help='Suppress output except warnings and errors.',
        )
        parser.add_argument(
            '-h', '--help',
            action=HelpAction,
            nargs=0,
            default=self,  # tricky
            help="Show this help message and exit.",
        )
        parser.add_argument(
            '--debug',
            default=False,
            action='store_true',
            help='Show tracebacks on errors.',
        )
        parser.add_argument(
            '--os-blog-url',
            action='store',
            dest='blog_url',
            default=c.env('OS_BLOG_URL',
                          default='http://localhost:8989/v1'),
            help='Blog API host (Env: OS_BLOG_URL)'
        )
        parser.add_argument(
            '--os-username',
            action='store',
            dest='username',
            default=c.env('OS_USERNAME', default='admin'),
            help='Authentication username (Env: OS_USERNAME)'
        )
        parser.add_argument(
            '--os-password',
            action='store',
            dest='password',
            default=c.env('OS_PASSWORD', default='root'),
            help='Authentication password (Env: OS_PASSWORD)'
        )
        parser.add_argument(
            '--os-tenant-id',
            action='store',
            dest='tenant_id',
            default=c.env('OS_TENANT_ID'),
            help='Authentication tenant identifier (Env: OS_TENANT_ID)'
        )
        parser.add_argument(
            '--os-tenant-name',
            action='store',
            dest='tenant_name',
            default=c.env('OS_TENANT_NAME', 'Default'),
            help='Authentication tenant name (Env: OS_TENANT_NAME)'
        )
        parser.add_argument(
            '--os-auth-token',
            action='store',
            dest='token',
            default=c.env('OS_AUTH_TOKEN'),
            help='Authentication token (Env: OS_AUTH_TOKEN)'
        )
        parser.add_argument(
            '--os-auth-url',
            action='store',
            dest='auth_url',
            default=c.env('OS_AUTH_URL'),
            help='Authentication URL (Env: OS_AUTH_URL)'
        )
        parser.add_argument(
            '--os-cacert',
            action='store',
            dest='cacert',
            default=c.env('OS_CACERT'),
            help='Authentication CA Certificate (Env: OS_CACERT)'
        )
        return parser

    def initialize_app(self, argv):
        self._clear_shell_commands()

        ver = client.determine_client_version(self.options.blog_url)

        self._set_shell_commands(self._get_commands(ver))

        self.client = client.client(blog_url=self.options.blog_url,
                                    username=self.options.username,
                                    api_key=self.options.password,
                                    project_name=self.options.tenant_name,
                                    auth_url=self.options.auth_url,
                                    project_id=self.options.tenant_id,
                                    endpoint_type='publicURL',
                                    service_type='blog',
                                    auth_token=self.options.token,
                                    cacert=self.options.cacert)

    def _set_shell_commands(self, cmds_dict):
        for k, v in cmds_dict.items():
            self.command_manager.add_command(k, v)

    def _clear_shell_commands(self):
        exclude_cmds = ['help', 'complete']

        cmds = self.command_manager.commands.copy()
        for k, v in cmds.items():
            if k not in exclude_cmds:
                self.command_manager.commands.pop(k)

    def _get_commands(self, version):
        if version == 1:
            return self._get_commands_v1()

        return {}

    @staticmethod
    def _get_commands_v1():
        return {
            'blog-list': blogclient.commands.v1.blogs.List,
            'blog-get': blogclient.commands.v1.blogs.Get,
            'blog-create': blogclient.commands.v1.blogs.Create,
            'blog-delete': blogclient.commands.v1.blogs.Delete,
            'blog-update': blogclient.commands.v1.blogs.Update,
            'blog-create-json':blogclient.commands.v1.blogs.Add
        }


def main(argv=sys.argv[1:]):
    print argv
    print '--------------------'
    return BlogShell().run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
