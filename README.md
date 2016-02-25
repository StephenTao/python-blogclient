Blog client
==============

Python client for Blog REST API. Includes python library for Blog API and Command Line Interface (CLI) library.


Installation
------------

First of all, clone the repo and go to the repo directory:

    git clone git@git.augmentum.com.cn:Openstack-demo/python-blogclient.git
    cd python-blogclient

Then just run:

    pip install -e .

or

    python setup.py install


Running Blog client
----------------------

If Blog authentication is enabled, provide the information about OpenStack auth to environment variables. Type:

    export OS_AUTH_URL=http://127.0.0.1:5000/v3
    export OS_USERNAME=admin
    export OS_TENANT_NAME=admin
    export OS_PASSWORD=root
    export OS_Blog_URL=http://127.0.0.1:8989/v1

and in the case that you are authenticating against keystone over https:

    export OS_CACERT=<path_to_ca_cert>

>***Note:** In client, we can use both Keystone auth versions - v2.0 and v3. But server supports only v3.*

To make sure Blog client works, type:

    blog blog-list

You can see the list of available commands typing:

    blog --help
