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
from datetime import datetime, timedelta

class Queue:

    def __init__(self, cache):

        self.cache = cache
        self.expiration_times = {
            'tweets': timedelta(weeks=2)
        }

    def record_item_property(self, queue, item, prop, value):
        # retrieve the document
        doc = self.cache.get_document(queue, item)
        # set item property
        doc[prop] = value
        # save the document
        self.cache.put_document(queue, doc)

    def get_item_property(self, queue, item, prop):
        doc = self.cache.get_document(queue, item)
        if doc is not None:
            return doc.get(prop, None)
        else:
            return None

    def set_expiration(self, queue, time):
        # set an expiration time for a given queue
        self.expiration_times[queue] = time

    def queue_item(self, queue, item):
        # add the item to the specified queue, if it is not already present
        self.cache.put_document(queue, item)

    def record_item_property_check(self, queue, item, prop, timestamp=None):
        # record that the item in the queue has been checked at the given time
        # and check whether it has now expired
        if not timestamp:
            timestamp = time.time()

        docs = self.cache.get_documents(queue, item)

        for doc in docs:
        
            if not doc.get('%s_first_checked' % prop, None):
                doc['%s_first_checked' % prop] = timestamp
                
            doc['%s_last_checked' % prop] = timestamp
        
            self.cache.put_document(queue, doc)

            if self.expiration_times.get(queue, None):
                if datetime.fromtimestamp(doc['%s_last_checked' % prop]) - datetime.fromtimestamp(doc['%s_first_checked' % prop]) > self.expiration_times[queue]:
                    self.remove_item(queue, doc)

    def remove_item(self, queue, item):
        # remove the item from the queue
        self.cache.remove_document(queue, item)

    def get_queue(self, queue):
        # retrieve the specific queue
        return self.cache.get_collection(queue)

