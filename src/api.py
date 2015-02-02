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

def make_and_fire_request(url, data=None, headers=None, method="GET"):

    if data:
        data = urllib.urlencode(data)

    if method is "GET":
        url = url + "?" + data
        if headers:
            request = urllib2.Request(url, headers=headers)
        else:
            request = urllib2.Request(url)
    elif method is "POST":
        request = urllib2.Request(url, data, headers)

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

