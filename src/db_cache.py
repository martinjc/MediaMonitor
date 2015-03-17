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


from pymongo import *


class MongoDBCache(object):

    def __init__(self, mongo_server='mongodb://localhost:27017/', db='test'):

        self.client = MongoClient(mongo_server)
        self.db = self.client[db]

    def document_exists(self, collection, query):
        """
        Checks to see if a document matching the query exists within the database. 
        """

        item = self.db[collection].find_one(query)

        # item exists
        if item is not None:
            return True
        # item does not exist
        else:
            return False

    def get_document(self, collection, query):
        assert self.document_exists(collection, query)
        return self.db[collection].find_one(query)

    def get_documents(self, collection, query):
        return self.db[collection].find(query)

    def put_document(self, collection, data):
        return self.db[collection].save(data)

    def get_collection(self, collection):
        return self.db[collection]

    def remove_document(self, collection, query):
        assert self.document_exists(collection, query)
        return self.db[collection].remove(query)
