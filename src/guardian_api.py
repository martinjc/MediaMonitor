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

class Guardian_API:

    def __init__(self):

        scheme = "http://"
        api_url = "content.guardianapis.com"

        self.api_base = scheme + api_url + "/"
        self.api_key = gu_api_key


    def build_query(self, object_id, in_params=None):
        #
        # Params sanitising -- erase any tokens and client creds...
        if in_params:
            params = copy.copy(in_params)
            for fld in ["access_token","client_id","client_secret", "api_key"]:
                if fld in params:
                    del params[fld]
        else:
            params = {}

        params["api-key"] = self.api_key

        str_param_data = {}
        for k, v in params.iteritems():
            str_param_data[k] = unicode(v).encode("utf-8")

        url = self.api_base + "/" + object_id + "?" + urllib.urlencode(str_param_data)

        q = Query(url)
        print q.get_json()
        return q


    def query(self, object_id, in_params=None):

        query = self.build_query(object_id, in_params)
        return make_and_fire_request(query)

if __name__ == "__main__":

    gu_api = Guardian_API()
    params = {
        "show-fields": "all",
        "show-elements": "all",
        "show-references": "all",
        "show-tags": "all",
        "show-rights": "all",
        "page-size": 100,
        "order-by": "oldest",
        "from-date": "2006-01-01",
        "q": "recession"
    }
    results = gu_api.query("search", in_params=params)
    for result in results["response"]["results"]:
        print result["webTitle"], result["fields"]["publication"], result["webPublicationDate"]
    