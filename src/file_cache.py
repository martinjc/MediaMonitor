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


class FileCache(object):

    def __init__(self):
        # initialise the cache
        pass

    def document_exists(self, id):
        # check whether we have any instances of the given ID
        pass

    def get_document(self, id, timestamp=None):
        # get the document with the given id and the timestamp closest
        # to the given timestamp. default to the latest.
        pass

    def put_document(self, id, document, timestamp=None):
        # add the document to the id store with the given timestamp
        pass

    def remove_document(self, id, timestamp):
        # remove the given document with the given timestamp from the cache
