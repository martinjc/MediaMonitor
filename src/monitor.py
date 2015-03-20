import time
import threading
import multiprocessing

from twython import TwythonStreamer, Twython
from datetime import datetime, timedelta

from db_cache import *
from _credentials import *
from _sources import sources
from json_file_cache import TwitterFileCache

UPDATE_USER_LIST = timedelta(minutes=5)
UPDATE_PROFILES = timedelta(minutes=5)


# deal with streaming updates
class Streamer(TwythonStreamer):

    def __init__(self, cache, *args):
        """
        Initialise a connection to a database 
        to store returned tweets in
        """
        self.db_cache = cache
        TwythonStreamer.__init__(self, *args)

    def on_success(self, data):
        """
        Add a tweet to the database
        """
        self.db_cache.put_document('tweets', data)

    def on_error(self, status_code, data):
        """
        Output any errors
        """
        print(status_code)
        print(data)

    def end_stream(self):
        self.disconnect()


class StreamMonitor(object):

    def __init__(self):

        # file cache of twitter responses
        self.file_cache = TwitterFileCache()
        # DB cache
        self.db_cache = MongoDBCache(db='MediaMonitor')
        # API object for accessing Twitter API
        self.ts = Streamer(self.db_cache, twitter_client_id, twitter_client_secret, twitter_access_token, twitter_access_token_secret)
        # users
        self.users = ""

    def read_users(self):
        u = self.db_cache.get_collection('users')
        us = []
        for user in u:
            us.append(user['id_str'])
        self.users = ','.join(us)
        return len(us)

    def monitor_stream(self, users=None):
        if users is None:
            users = self.users
        self.ts.statuses.filter(follow=users, lang="en")

    def disconnect_stream(self):
        self.ts.end_stream()


class ProfileMonitor(object):

    def __init__(self):
        # file cache of twitter responses
        self.file_cache = TwitterFileCache()
        # DB cache
        self.db_cache = MongoDBCache(db='MediaMonitor')
        # Twitter API
        self.ta = Twython(twitter_client_id, twitter_client_secret, twitter_access_token, twitter_access_token_secret)
        
        # query limiting
        max_per_hour = 175 * 15
        query_interval = (60 * 60) / float(max_per_hour)   # in seconds
        
        self.monitor = {'wait': query_interval,
                        'earliest': None,
                        'timer': None}

    def __rate_controller(self, monitor_dict):
        if monitor_dict['timer'] is not None:
            monitor_dict['timer'].join()   # causes main thread to sit and wait

            # Waste time in the (unlikely) case that the timer thread finished early.
            while time.time() < monitor_dict['earliest']:
                time.sleep(monitor_dict['earliest'] - time.time())

        # Prepare for next call and start timer...
        earliest = time.time() + monitor_dict['wait']
        timer = threading.Timer(earliest-time.time(), lambda: None)
        monitor_dict['earliest'] = earliest
        monitor_dict['timer'] = timer
        monitor_dict['timer'].start()

    def update_profiles(self):
        u = self.db_cache.get_collection('users')
        users = []
        for user in u:
            users.append(user['id_str'])

        start = 0
        end = 0

        while end < len(users):
            start = end
            if end + 99 < len(users):
                end = end + 99
            else:
                end = len(users)

            ids = ",".join(users[start:end])
            user_content = query_user_lookup(ids)
            for user in user_content:
                if user["protected"] != 'true':
                    self.file_cache.put_profile(user)
                    self.db_cache.put_document('users', user) 

    def query_user_lookup(self, ids):
        self.__rate_controller(self.monitor)
        user_content = self.ta.lookup_user(user_id=ids)

        if ta.get_lastfunction_header('x-rate-limit-remaining') == 0:
            self.monitor['earliest'] = float(ta.get_lastfunction_header['x-rate-limit-reset'])
            return self.query_user_lookup(ids)
        else:
            return user_content

if __name__ == "__main__":

    sm = StreamMonitor()
    pm = ProfileMonitor()

    print("updating user list")
    num_users = sm.read_users()
    print("currently tracking: %d" % (num_users))
    p = multiprocessing.Process(target=sm.monitor_stream)
    p.daemon = True
    print("starting stream")
    p.start()

    start_time = datetime.today()

    while(True):
        
        current_time = datetime.today()
        if current_time - start_time > UPDATE_PROFILES:
            print("updating profiles")
            pm.update_profiles()

        current_time = datetime.today()
        if current_time - start_time > UPDATE_USER_LIST:
            print("killing stream")
            p.terminate()
            print("currently tracking: %d" % (num_users))
            print("updating user list")
            num_users = sm.read_users()
            print("now tracking: %d" % (num_users))
            p = multiprocessing.Process(target=sm.monitor_stream)
            p.daemon = True
            print("starting stream")
            p.start()

    p.join()
