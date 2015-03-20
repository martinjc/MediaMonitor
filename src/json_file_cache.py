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


class TwitterFileCache(object):

    def __init__(self, cache_dir="data"):
        # initialise the cache
        self.cache_dir = os.path.join(os.getcwd(), cache_dir)

    def put_profile(self, profile, timestamp=None):

        if timestamp is None:
            timestamp = time.time()

        user_dir = os.path.join(self.cache_dir, profile['id_str'])

        if not os.path.isdir(user_dir):
            os.makedirs(user_dir)

        file_id = "profile_%f.json" % timestamp
        with open(os.path.join(user_dir, file_id), "w") as outfile:
            json.dump(profile, outfile)

