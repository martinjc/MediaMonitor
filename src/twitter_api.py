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

import time
import threading

import oauth2 as oauth

from api import *
from _credentials import *

class Twitter_API:

    def __init__(self):

        #
        # URL for accessing API
        scheme = "https://"
        api_url = "api.twitter.com"
        version = "1.1"

        self.api_base = scheme + api_url + "/" + version

        #
        # access credentials
        self.client_id = twitter_client_id
        self.client_secret = twitter_client_secret
        self.access_token = twitter_access_token
        self.access_secret = twitter_access_token_secret

        #
        # oauth tokens
        self.consumer = oauth.Consumer(key=self.client_id, secret=self.client_secret)
        self.token = oauth.Token(key=self.access_token, secret=self.access_secret)
        self.client = oauth.Client(self.consumer, self.token)

        #
        # query limiting
        max_per_hour = 180 * 15
        query_interval = (60 * 60) / float(max_per_hour)   # in seconds
        # The time to wait between issuing queries
        
        self.monitor = {'wait': query_interval,
                        'earliest': None,
                        'timer': None}

    def __rate_controller(self, monitor_dict):
        """
        Internal function to delay time as necessary. 
        This is general: depending on the `monitor_dict`, either the
        userless queries or the authenticated queries can be delayed.
        
        The methods functions as follows:
        1. join the timer that has been elapsing in the background.
        2. if the timer still hasn't finished yet, then we wait for it
          (causing the main thread to pause here too).
        3. update the monitor for the next delay. start the background timer.
        
        Fields of the monitor dictionary will be updated by this method.
        Dictionary fields understood as follows:
         * wait: the amount of time to wait between queries.
         * earliest: the earliest time that the next query should be issued.
         * timer: a backround thread that monitors the time for this particular
                  delay.
        """
        #
        # Cause main thread to wait until the desired time has elapsed.
        # If this is the first query for this monitor, then the timer is None
        # and we don't do any waiting.
        if monitor_dict['timer'] is not None:
            monitor_dict['timer'].join()   # causes main thread to sit and wait
                                           # for this monitor to elapse

            # Waste time in the (unlikely) case that the timer thread finished
            # early.
            while time.time() < monitor_dict['earliest']:
                time.sleep(monitor_dict['earliest'] - time.time())

        #
        # Prepare for next call and start timer...
        earliest = time.time() + monitor_dict['wait']
        timer = threading.Timer(earliest-time.time(), lambda: None)
        monitor_dict['earliest'] = earliest
        monitor_dict['timer'] = timer
        monitor_dict['timer'].start()


    def query(self, url, method="GET", data=None, headers=None):

        # rate limiting
        self.__rate_controller(self.monitor)

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


