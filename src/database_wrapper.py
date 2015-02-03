#!/usr/bin/env python
#
# Copyright 2011 Martin J Chorley & Matthew J Williams
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


from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlite3 import dbapi2 as sqlite
from database import *

MODULE = sqlite
DEBUG = False


class DBWrapper(object):

    def __init__(self, database):
        self.database = database
        Session = sessionmaker(bind=self._get_engine())
        self.session = Session()
    
    def _get_engine(self):
        return create_engine(self.database, module=MODULE, echo=DEBUG)

    def __create_tables__(self):
        """
        Sets up database tables.
        """
        engine = self._get_engine()
        if not engine.has_table('twitterusers'):
            engine.create(TwitterUser.__table__)
        if not engine.has_table('tweets'):
            engine.create(Tweet.__table__)

if __name__ == "__main__":

    db = DBWrapper("sqlite:///db.db")
    db.__create_tables__()
