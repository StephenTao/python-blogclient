# Copyright 2013 - Mirantis, Inc.
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

import six

from blogclient.api.v1 import client as client_v1


def client(blog_url=None, username=None, api_key=None,
           project_name=None, auth_url=None, project_id=None,
           endpoint_type='publicURL', service_type='workflow',
           auth_token=None, user_id=None, cacert=None):

        if blog_url and not isinstance(blog_url, six.string_types):
            raise RuntimeError('Blog url should be a string.')

        if not blog_url:
            blog_url = "http://localhost:8989/v1"

        return client_v1.Client(
            blog_url=blog_url,
            username=username,
            api_key=api_key,
            project_name=project_name,
            auth_url=auth_url,
            project_id=project_id,
            endpoint_type=endpoint_type,
            service_type=service_type,
            auth_token=auth_token,
            user_id=user_id,
            cacert=cacert
        )


def determine_client_version(blog_url):
    if blog_url.find("v1") != -1:
        return 1

    raise RuntimeError("Can not determine blog API version")
