#!/usr/bin/env python
#
# Copyright 2015  Martin J Chorley
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

from db_cache import *

import time
from datetime import datetime

class Queue:

    def __init__(self, cache):

        self.cache = cache
        # in secondss
        self.expiration_times = {}

    def set_expiration(self, queue, time):
        # set an expiration time for a given queue
        self.expiration_times[queue] = time

    def queue_item(self, queue, item):
        # add the item to the specified queue, if it is not already present
        self.cache.put_document(queue, item)

    def record_item_check(self, queue, item, timestamp=None):
        # record that the item in the queue has been checked at the given time
        # and check whether it has now expired
        if not timestamp:
            timestamp = time.time()

        doc = self.cache.get_document(queue, item)
        
        if not doc.get('first_checked', None):
            doc['first_checked'] = timestamp
            
        doc['last_checked'] = timestamp
        
        self.cache.put_document(queue, doc)

        if self.expiration_times.get(queue, None): 
            if datetime.fromtimestamp(doc['last_checked']) - datetime.fromtimestamp(doc['first_checked']) > self.expiration_times[queue]:
                self.remove_item(queue, doc)

    def remove_item(self, queue, item):
        # remove the item from the queue
        self.cache.remove_document(queue, item)

    def get_queue(self, queue):
        # retrieve the specific queue
        return self.cache.get_collection(queue)

