#!/usr/bin/env python
#
# Copyright 2014 Martin J Chorley
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


import json
import copy
import urllib
import urllib2

from api import *
from _credentials import *

class Facebook_API:

    def __init__(self):

        scheme = "https://"
        api_url = "graph.facebook.com"
        version = "v2.1"

        self.api_base = scheme + api_url + "/" + version


    def acquire_access_token(self):

        params = {
            "client_id": fb_client_id,
            "client_secret": fb_client_secret,
            "grant_type": "client_credentials"
        }

        str_param_data = {}
        for k, v in params.iteritems():
            str_param_data[k] = unicode(v).encode("utf-8")

        url = self.api_base + "/oauth/access_token"  + "?" + urllib.urlencode(str_param_data)

        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            raise e
        except urllib2.URLError, e:
            raise e

        raw_data = response.read()
        headers = response.info()

        access_token = raw_data[(raw_data.find("=")+1):]
        self.access_token = access_token
        return self.access_token

    def build_query(self, object_id, aspect=None, in_params=None):
        #
        # Params sanitising -- erase any tokens and client creds...
        if in_params:
            params = copy.copy(in_params)
            for fld in ["access_token","client_id","client_secret"]:
                if fld in params:
                    del params[fld]
        else:
            params = {}

        params["access_token"] = self.access_token

        str_param_data = {}
        for k, v in params.iteritems():
            str_param_data[k] = unicode(v).encode("utf-8")

        if aspect:
            url = self.api_base + "/" + object_id + "/" + aspect + "?" + urllib.urlencode(str_param_data)
        else:
            url = self.api_base + "/" + object_id + "?" + urllib.urlencode(str_param_data)

        q = Query(url)
        print q.get_json()
        return q


    def query(self, object_id, aspect=None, in_params=None):

        #
        # make sure we're authorised for querying
        if not self.access_token:
            self.acquire_access_token()

        query = self.build_query(object_id, aspect, in_params)
        return make_and_fire_request(query)

if __name__ == "__main__":

    fb_api = Facebook_API()
    fb_api.acquire_access_token()
    guardian_id = "10513336322"
    print fb_api.query(guardian_id)
    print fb_api.query(guardian_id, "posts", {"summary": True})
    