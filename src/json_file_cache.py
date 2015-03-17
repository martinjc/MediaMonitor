#!/usr/bin/env python
#
# Copyright 2015 Martin J Chorley
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

import os
import time
import json


class JSONFileCache(object):

    def __init__(self, cache_dir="data"):
        # initialise the cache
        self.cache_dir = os.path.join(os.getcwd(), cache_dir)

    def document_exists(self, item_id):
        # check whether we have any instances of the given ID
        item_dir = os.path.join(self.cache_dir, item_id)
        if os.path.isdir(item_dir):
            return os.listdir(item_dir)
        else:
            return False     

    def get_document(self, item_id, timestamp=None):
        # get the document with the given id and the timestamp closest
        # to the given timestamp. default to the latest.
        assert self.document_exists(item_id)
        item_dir = os.path.join(self.cache_dir, item_id)
        cache_items = sorted(os.listdir(item_dir))
        if timestamp is None:
            return json.load(open(cache_items[-1]))
        else:
            count = 0
            while timestamp < cache_items[count]:
                count += 1
            return json.load(open(cache_items[count]))

    def put_document(self, item_id, document, timestamp=None):
        # add the document to the id store with the given timestamp
        if timestamp is None:
            timestamp = time.time()
        item_dir = os.path.join(self.cache_dir, item_id)
        file_id = "%f.json" % timestamp
        with open(os.path.join(item_dir, file_id), "w") as outfile:
            json.dump(document, outfile)
