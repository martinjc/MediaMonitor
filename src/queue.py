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

    def record_item_check(self, queue, item, time):
        # record that the item in the queue has been checked at the given time
        # and check whether it has now expired
        self.cache.get_document(queue, item)
        if item.get('first_checked', None):
            first_checked = item['first_checked']
        else:
            item['first_checked'] = time

        if self.expiration_times.get('queue', None): 
            item['last_checked'] = time
            if time.ctime(item['last_checked']) - time.ctime(item['first_checked']) > self.expiration_times[queue]:
                self.remove_item(queue, item)

    def remove_item(self, queue, item):
        # remove the item from the queue
        self.cache.remove_document(queue, item)

    def get_queue(self, queue):
        # retrieve the specific queue
        self.cache.get_collection(queue)


