import json
import urllib

from db_cache import *
from queue import *
from twitter_api import Twitter_API
from json_file_cache import JSONFileCache

from datetime import timedelta, datetime

SEED_CHECK = timedelta(hours=12)
LATEST_TWEET_CHECK = timedelta(hours=2)

TWEET_CHECK = timedelta(hours=6)


class Monitor(object):

    def __init__(self):

        # queue of objects to check
        self.queue = Queue(MongoDBCache(db='MediaMonitor'))
        # file cache of twitter responses
        self.file_cache = JSONFileCache()
        # API object for accessing Twitter API
        self.ta = Twitter_API()  

    def get_tweet_history(self, user):

        # make an api call to get the most recent tweets of the am
        params = {
            "screen_name": user,
            "count": 200,
            "exclude_replies": "false"
        }

        tweets_api = self.ta.api_base + "/" + "statuses" + "/" + "user_timeline" + ".json"
        tweets = json.loads(self.ta.query(tweets_api, "GET", data=urllib.urlencode(params)))

        # # find the earliest tweet retrieved
        # if len(tweets) > 0:
        #     earliest_id = tweets[0]["id"]
        #     for tweet in tweets:
        #         if tweet["id"] < earliest_id:
        #             earliest_id = tweet["id"]

        #     # assume there are more tweets to retrieve
        #     more_tweets = False

        #     # while there are more tweets to retrieve
        #     while(more_tweets):

        #         # make an api call to get the tweets prior 
        #         # to our earliest retrieved tweet so far
        #         params = {
        #             "screen_name": user,
        #             "count": 200,
        #             "exclude_replies": "false",
        #             "max_id": earliest_id
        #         }

        #         new_tweets = json.loads(self.ta.query(tweets_api, "GET", data=urllib.urlencode(params)))

        #         # add the newly retrieved tweets to our list
        #         tweets.extend(new_tweets)

        #         # find the earliest retrieved tweet
        #         current_earliest = earliest_id
        #         for tweet in tweets:
        #             if tweet["id"] < earliest_id:
        #                 earliest_id = tweet["id"]

        #         # if the earliest tweet hasn't changed
        #         # we can't go back any further
        #         if current_earliest == earliest_id:
        #             more_tweets=False

        return tweets

    def get_latest_tweets(self, user, latest_id):

        tweets = []

        # make a call and find the latest tweets
        params = {
            "screen_name": user,
            "count": 200,
            "exclude_replies": "false",
            "since_id": latest_id
        }

        tweets_api = self.ta.api_base + "/" + "statuses" + "/" + "user_timeline" + ".json"
        new_tweets = json.loads(self.ta.query(tweets_api, "GET", data=urllib.urlencode(params)))

        # add any new tweets to our set of tweets
        tweets.extend(new_tweets)
        # assume there's more
        more_tweets = True

        # find the latest tweet
        for tweet in tweets:
            if tweet["id"] > latest_id:
                latest_id = tweet["id"]

        while more_tweets:

            # make a call and find the latest tweets
            params = {
                "screen_name": user,
                "count": 200,
                "exclude_replies": "false",
                "since_id": latest_id
            }
            new_tweets = json.loads(self.ta.query(tweets_api, "GET", data=urllib.urlencode(params)))

            # add any new tweets to our set of tweets
            tweets.extend(new_tweets)

            current_latest = latest_id
            # find the latest tweet
            for tweet in tweets:
                if tweet["id"] > latest_id:
                    latest_id = tweet["id"]

            if current_latest == latest_id:
                more_tweets = False

        return tweets

    def remove_tweet_duplicates(tweets):

        tweet_ids = []
        to_remove = []
        # go through all the tweets
        for tweet in tweets:
            # if we've already seen this tweet
            if tweet["id"] in tweet_ids:
                # add it to the list of tweets to remove
                to_remove.append(tweet)
            else:
                # otherwise add the ID to the list of tweets we've seen
                tweet_ids.append(tweet["id"])

        for tweet in to_remove:
            tweets.remove(tweet)

        return tweets

    def check_twitter_seeds(self):

        # retrieve all seeds
        seeds = self.queue.get_queue('twitter_seeds')

        profiles_to_check = []
        latest_tweets_to_check = []

        # check all users for those that need updates
        for seed in seeds:
            if not seed.get('profile_last_checked', None):
                profiles_to_check.append(seed['screen_name'])
            else:
                last_checked = seed['profile_last_checked']
                now = datetime.today()
                if now - datetime.fromtimestamp(last_checked) > SEED_CHECK:
                    profiles_to_check.append(seed['screen_name'])

            if not seed.get('tweets_last_checked', None):
                latest_tweets_to_check.append(seed['screen_name'])
            else:
                last_checked = seed['tweets_last_checked']
                now = datetime.today()
                if now - datetime.fromtimestamp(last_checked) > LATEST_TWEET_CHECK:
                    latest_tweets_to_check.append(seed['screen_name'])

        print(profiles_to_check)
        print(latest_tweets_to_check)
        print(len(latest_tweets_to_check))

        if len(profiles_to_check) > 0:
            self.check_profile(profiles_to_check)

        if len(latest_tweets_to_check) > 0:
            self.check_seed_tweets(latest_tweets_to_check)

    def check_profile(self, users):

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
                self.queue.record_item_property_check('twitter_seeds', {'screen_name': user['screen_name']}, 'profile')
                
    def check_seed_tweets(self, users):

        # get the latest tweet stored for the user
        for user in users:
            latest_tweet = self.queue.get_item_property('twitter_seeds', {'screen_name': user}, 'latest_tweet')
            if latest_tweet is None:
                tweets = self.get_tweet_history(user)
            else:
                tweets = self.get_latest_tweets(user, latest_tweet)

            latest_id = 0
            for tweet in tweets:
                if tweet["id"] > latest_id:
                    latest_id = tweet["id"]
                self.file_cache.put_document('tweets', tweet['id_str'], tweet)
                self.queue.queue_item('tweets', {'tweet_id': tweet['id_str']})

            for tweet in tweets:
                self.queue.record_item_property('twitter_seeds', {'screen_name': user}, 'latest_tweet', latest_id)
                self.queue.record_item_property_check('tweets', {'tweet_id': tweet['id_str']}, 'profile')
            self.queue.record_item_property_check('twitter_seeds', {'screen_name': user}, 'tweets')

    def check_tweets(self):
        # retrieve all seeds
        tweets = self.queue.get_queue('tweets')

        tweets_to_check = []
        

        # check all users for those that need updates
        for tweet in tweets:
            if not tweet.get('profile_last_checked', None):
                tweets_to_check.append(tweet['tweet_id'])
            else:
                last_checked = tweet['profile_last_checked']
                now = datetime.today()
                if now - datetime.fromtimestamp(last_checked) > TWEET_CHECK:
                    tweets_to_check.append(tweet['tweet_id'])
        
        print(len(tweets_to_check))
        tweets_to_check = remove_tweet_duplicates(tweets_to_check)
        print(len(tweets_to_check))

        if len(tweets_to_check) > 0:
            self.check_tweet_profiles(tweets_to_check)

    def check_tweet_profiles(self, tweets):

        start = 0
        end = 0

        while end < len(tweets):
            start = end
            if end + 99 < len(tweets):
                end = end + 99
            else:
                end = len(tweets)

            params = {
                "id": ",".join(tweets[start:end])
            }

            tweet_lookup_api = self.ta.api_base + "/" + "statuses" + "/" + "lookup" + ".json"
            tweet_content = json.loads(self.ta.query(tweet_lookup_api, "POST", data=urllib.urlencode(params)))
            for tweet in tweet_content:
                self.file_cache.put_document('tweets', tweet["id_str"], tweet)
                self.queue.record_item_property_check('tweets', {'tweet_id': tweet['id_str']}, 'profile')


if __name__ == "__main__":

    monitor = Monitor()

    while(True):

        # update user profiles
        monitor.check_twitter_seeds()

        # check all tweets for those that need updates
        monitor.check_tweets()

    # check all entities for those that need updates
    # update entities