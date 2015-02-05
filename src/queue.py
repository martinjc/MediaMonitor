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


class Queue:

    def __init__(self, cache):

        self.cache = cache
        self.expiration_times = {}

    def set_expiration(self, queue, time):
        # set an expiration time for a given queue
        pass

    def queue_item(self, queue, item):
        # add the item to the specified queue, if it is not already present
        pass

    def record_item_check(self, queue, item, time):
        # record that the item in the queue has been checked at the given time
        # and check whether it has now expired
        pass

    def remove_item(self, queue, item):
        # remove the item from the queue
        pass

    def get_queue(self, queue):
        # retrieve the specific queue
        pass


