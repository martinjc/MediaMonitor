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
import base64
import urllib
import urllib2

from collections import defaultdict
from datetime import datetime

from api import *
from _credentials import *

class Twitter_API:

    def __init__(self):

        # URL for accessing API
        scheme = "https://"
        api_url = "api.twitter.com"
        version = "1.1"

        self.api_base = scheme + api_url + "/" + version

        # seconds between queries to each endpoint
        query_intervals = {
            "statuses/lookup": (15 * 60) / 60,               # 60 requests per 15 minute window (app authentication) 
            "users/lookup": (15 * 60) / 60                    # 60 requests per 15 minute window (app authentication) 
        }

        # internal monitoring of time for rate-limiting
        self.timers = defaultdict(datetime)

        for endpoint, interval in query_intervals.iteritems():
            self.timers[endpoint] = { "delay": interval,
                                        "earliest": None}

        # queue of requests to process
        self.queue = defaultdict(list)

        # authorise the API object to access the API
        self.acquire_access_token()


    def acquire_access_token(self):

        client_id = twitter_client_id
        client_secret = twitter_client_secret

        bearer_credentials = "%s:%s" % (client_id, client_secret)
        encoded_bearer_credentials = base64.b64encode(bearer_credentials)

        params = {
            "grant_type": "client_credentials"
        }

        data = urllib.urlencode(params)
        url = "https://api.twitter.com/oauth2/token"
        headers = { "Authorization": "Basic %s" % encoded_bearer_credentials, "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}

        request = urllib2.Request(url, data, headers)

        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            raise e
        except urllib2.URLError, e:
            raise e

        raw_data = response.read()
        json_data = json.loads(raw_data)

        self.access_token = json_data["access_token"]

    def build_query(self, endpoint, aspect, in_params=None):
        #
        # Params sanitising -- erase any tokens and client credentials...
        if in_params:
            params = copy.copy(in_params)
            for fld in ["access_token","client_id","client_secret"]:
                if fld in params:
                    del params[fld]
        else:
            params = {}

        str_param_data = {}
        for k, v in params.iteritems():
            str_param_data[k] = unicode(v).encode("utf-8")

        #
        # gather parameters for POST request
        url = self.api_base + "/" + endpoint + "/" + aspect + ".json"
        data = str_param_data
        headers = {"Authorization": "Bearer %s" % (self.access_token)}

        q = Query(url, data, headers)  
        print q.get_json()
        return q

    def query(self, endpoint, aspect, in_params=None):

        #
        # make sure we're authorised for querying
        if not self.access_token:
            self.acquire_access_token()

        full_endpoint = endpoint + "/" + aspect




        query = self.build_query(endpoint, aspect, in_params)

        #
        # make the request
        response = make_and_fire_request(query)
        print response

    def run(self):



if __name__ == "__main__":

    ta = Twitter_API()
    ta.acquire_access_token()
    params = {"screen_name" : "BBCNews,BBCBreaking,BBCWorld"}
    ta.query("users", "lookup", params)

