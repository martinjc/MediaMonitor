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

"""
API makes all HTTP requests
"""

class Query:

    def __init__(self, url, data=None, headers=None, method="GET"):

        self.url = url
        self.data = data
        self.headers = headers
        self.method = method

    def get_json(self):
        data = {}
        data["url"] = self.url
        data["data"] = self.data
        data["headers"] = self.headers
        data["method"] = self.method
        return json.dumps(data)

    def build_query(json_str):
        query_data = json.loads(json_str)
        return Query(url=query_data["url"], data=query_data["data"], headers=query_data["headers"], method=query_data["method"])



def make_and_fire_request(query):

    if query.data:
        query.data = urllib.urlencode(query.data)

    if query.method is "GET":
        query.url = query.url + "?" + query.data
        if query.headers:
            request = urllib2.Request(query.url, headers=query.headers)
    elif query.method is "POST":
        request = urllib2.Request(query.url, query.data, query.headers)

    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        print e
        raise e
    except urllib2.URLError as e:
        print e
        raise e

    raw_data = response.read()
    return json.loads(raw_data)



