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
import logging

"""

API makes all HTTP requests. It logs success and failure, 
and reports failure to admins

"""
class Query:

    def __init__(self, url, data=None, headers=None):

        self.url = url
        self.data = data
        self.headers = headers

    def get_json(self):
        data = {}
        data["url"] = self.url
        data["data"] = self.data
        data["headers"] = self.headers
        return json.dumps(data)

    def build_query(json_str):
        query_data = json.loads(json_str)
        return Query(url=query_data["url"], data=query_data["data"], headers=query_data["headers"])



def make_and_fire_request(query):

    logging.info("[API] [POST] Requesting: %s" % (query.url))

    if query.data:
        query.data = urllib.urlencode(query.data)

    if query.headers:
        request = urllib2.Request(query.url, query.data, query.headers)
    else:
        request = urllib2.Request(query.url, query.data)

    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        logging.warning("[API] ERROR: %s" % (e))
        print e
        raise e
    except urllib2.URLError, e:
        logging.info("[API] ERROR: %s" % (e))
        print e
        raise e

    raw_data = response.read()
    logging.info("[API] response received")
    return json.loads(raw_data)
  

"""
TODO: implement this!
"""
def _handle_error(e):
    raise e


