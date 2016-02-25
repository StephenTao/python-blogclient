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

from blogclient.api import base


class Blog(base.Resource):
    resource_name = 'Blog'


class BlogManager(base.ResourceManager):
    resource_class = Blog

    def add(self, definition):
        if (len(definition) <= 0):
            return
        resp = self.client.http_client.post('/blogs', definition)
        return resp

    def create(self, definition):

        self._ensure_not_empty(definition=definition)
        if (type(definition) != dict):
            definition = {'id':55,'title':'test1','content':'content1'}

        resp = self.client.http_client.post(
            '/blogs',
            definition,
            headers={'content-type': 'application/json'}
        )

        if resp.status_code != 201:
            self._raise_api_exception(resp)

        return self.resource_class(self, base.extract_json(resp, None))

    def update(self, definition):
        self._ensure_not_empty(definition=definition)
        if (type(definition) != dict):
            definition = {'id':55,'title':'test1','content':'content1'}
        print definition
        resp = self.client.http_client.put(
            '/blogs',
            definition,
            headers={'content-type': 'application/json'}
        )

        if resp.status_code != 200:
            self._raise_api_exception(resp)

        return self.resource_class(self, base.extract_json(resp, None))

    def list(self):
        return self._list('/blogs', response_key='blogs')

    def get(self, title):
        self._ensure_not_empty(title=title)

        return self._get('/blogs/%s' % title)

    def delete(self, title):
        self._ensure_not_empty(title=title)

        self._delete('/blogs/%s' % title)

    def validate(self, definition):
        self._ensure_not_empty(definition=definition)

        resp = self.client.http_client.post(
            '/blogs/validate',
            definition,
            headers={'content-type': 'application/json'}
        )

        if resp.status_code != 200:
            self._raise_api_exception(resp)

        return base.extract_json(resp, None)
