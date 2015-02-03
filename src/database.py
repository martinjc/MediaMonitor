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

from datetime import datetime, timedelta

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import BIGINT

Base = declarative_base()

class TwitterUser(Base):
    __tablename__ = 'twitterusers'

    id = Column(BIGINT, primary_key=True)
    profile_last_checked = Column(DateTime)
    profile_next_check = Column(DateTime)
    tweets_last_checked = Column(DateTime)
    tweets_next_check = Column(DateTime)

    def __init__(self, id, check_time):

        one_day = timedelta(hours=1)
        four_hours = timedelta(hours=4)

        self.id = id
        self.profile_last_checked = check_time
        self.profile_next_check = check_time + one_day
        self.tweets_last_checked = check_time
        self.tweets_next_check = check_time + four_hours


class Tweet(Base):
    __tablename__ = 'tweets'
    id = Column(BIGINT, primary_key=True)
    created = Column(DateTime)
    last_checked = Column(DateTime)
    next_check = Column(DateTime)

    def __init__(self, id, created, check_time):

        one_day = timedelta(hours = 1)

        self.id = id
        self.created = created
        self.last_checked = check_time
        self.next_check = check_time + one_day


