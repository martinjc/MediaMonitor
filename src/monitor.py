import json
import urllib

from db_cache import *
from queue import *
from twitter_api import Twitter_API
from json_file_cache import JSONFileCache

from datetime import timedelta, datetime


SEED_CHECK = timedelta(days=1)


class Monitor(object):

    def __init__(self):

        # queue of objects to check
        self.queue = Queue(MongoDBCache(db='MediaMonitor'))

        # file cache of twitter responses
        self.file_cache = JSONFileCache()

        # API object for accessing Twitter API
        self.ta = Twitter_API()       

    def check_twitter_seeds(self, users):

        start = 0
        end = 0

        while end < len(users):
            start = end
            if end + 99 < len(users):
                end = end + 99
            else:
                end = len(users)

            params = {
                "screen_name": ",".join(users[start:end])
            }
            users_lookup_api = self.ta.api_base + "/" + "users" + "/" + "lookup" + ".json"
            user_content = json.loads(self.ta.query(users_lookup_api, "POST", data=urllib.urlencode(params)))
            for user in user_content:
                self.file_cache.put_document('twitter_seeds', user["id_str"], user)
                self.queue.record_item_check('twitter_seeds', {'screen_name': user['screen_name']})


if __name__ == "__main__":

    monitor = Monitor()

    #while(true):

    # retrieve all users
    seeds = monitor.queue.get_queue('twitter_seeds')

    to_check = []

    # check all users for those that need updates
    for seed in seeds:
        if not seed.get('last_checked', None):
            to_check.append(seed['screen_name'])
        else:
            last_checked = seed['last_checked']
            now = datetime.today()
            if now - last_checked > SEED_CHECK:
                to_check.append(seed['screen_name'])
    
    print(to_check)
    # update user profiles
    monitor.check_twitter_seeds(to_check)


    # get latest user tweets
    # update user tweet store
    # for all tweets in user tweets:
        # add tweet to tweet queue
        # add any urls to entity queue

    # check all tweets for those that need updates
    # update tweets

    # check all entities for those that need updates
    # update entities