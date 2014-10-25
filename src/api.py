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

def make_and_fire_get_request(url):

    logging.info("[API] Requesting: %s" % (url))
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        logging.warning("[API] ERROR: %s" % (e))
        raise e
    except urllib2.URLError, e:
        logging.info("[API] ERROR: %s" % (e))
        raise e

    raw_data = response.read()
    logging.info("[API] response received")
    return json.loads(raw_data)


def make_and_fire_post_request(url, data, headers):

    logging.info("[API] [POST] Requesting: %s" % (url))

    data = urllib.urlencode(data)

    request = urllib2.Request(url, data, headers)

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


