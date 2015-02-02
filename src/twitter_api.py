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


import oauth2 as oauth
import time
import urlparse

from api import *
from _credentials import *

class Twitter_API:

    def __init__(self):

        # URL for accessing API
        scheme = "https://"
        api_url = "api.twitter.com"
        version = "1.1"

        self.api_base = scheme + api_url + "/" + version

        self.client_id = twitter_client_id
        self.client_secret = twitter_client_secret
        self.access_token = twitter_access_token
        self.access_secret = twitter_access_token_secret

        self.consumer = oauth.Consumer(key=self.client_id, secret=self.client_secret)
        self.token = oauth.Token(key=self.access_token, secret=self.access_secret)
        self.client = oauth.Client(self.consumer, self.token)


    def query(self, url, method="GET", data=None, headers=None):

        response, content = self.client.request(url, method, body=data, headers=headers)
        if response['status'] == '200':
            return content
        else:
            return None



if __name__ == "__main__":

    ta = Twitter_API()
    params = {"screen_name" : "BBCNews,BBCBreaking,BBCWorld"}

    users_lookup_api = ta.api_base + "/" + "users" + "/" + "lookup" + ".json"

    content = ta.query(users_lookup_api, "POST", data=urllib.urlencode(params))
    print(content)


