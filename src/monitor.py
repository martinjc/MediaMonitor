import json
import urllib

from db_cache import *
from queue import *
from twitter_api import Twitter_API
from json_file_cache import JSONFileCache

from datetime import timedelta, datetime


SEED_CHECK = timedelta(days=1)
TWEET_CHECK = timedelta(hours=1)


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
        tweets = json.loads(self.ta.query(tweets_api, "POST", data=urllib.urlencode(params)))

        # find the earliest tweet retrieved
        if len(tweets) > 0:
            earliest_id = tweets[0]["id"]
            for tweet in tweets:
                if tweet["id"] < earliest_id:
                    earliest_id = tweet["id"]

            # assume there are more tweets to retrieve
            more_tweets = True

            # while there are more tweets to retrieve
            while(more_tweets):

                # make an api call to get the tweets prior 
                # to our earliest retrieved tweet so far
                params = {
                    "screen_name": user,
                    "count": 200,
                    "exclude_replies": "false",
                    "max_id": earliest_id
                }

                new_tweets = json.loads(self.ta.query(tweets_api, "POST", data=urllib.urlencode(params)))

                # add the newly retrieved tweets to our list
                tweets.extend(new_tweets)

                # find the earliest retrieved tweet
                current_earliest = earliest_id
                for tweet in tweets:
                    if tweet["id"] < earliest_id:
                        earliest_id = tweet["id"]

                # if the earliest tweet hasn't changed
                # we can't go back any further
                if current_earliest == earliest_id:
                    more_tweets=False

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
        new_tweets = json.loads(self.ta.query(tweets_api, "POST", data=urllib.urlencode(params)))

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
            new_tweets = json.loads(self.ta.query(tweets_api, "POST", data=urllib.urlencode(params)))
            new_tweets = api.query_get("statuses", "user_timeline", params)

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

        to_check = []

        # check all users for those that need updates
        for seed in seeds:
            if not seed.get('last_checked', None):
                to_check.append(seed['screen_name'])
            else:
                last_checked = seed['last_checked']
                now = datetime.today()
                if now - datetime.fromtimestamp(last_checked) > SEED_CHECK:
                    to_check.append(seed['screen_name'])

        print(to_check)

        self.check_profile(to_check)
        self.check_seed_tweets(to_check)

        for user in seeds:
            self.queue.record_item_check('twitter_seeds', {'screen_name': user['screen_name']})

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
                "screen_name": ",".join(to_check[start:end])
            }
            users_lookup_api = self.ta.api_base + "/" + "users" + "/" + "lookup" + ".json"
            user_content = json.loads(self.ta.query(users_lookup_api, "POST", data=urllib.urlencode(params)))
            for user in user_content:
                self.file_cache.put_document('twitter_seeds', user["id_str"], user)
                

    def check_seed_tweets(self, user):

        # get the latest tweet stored for the user
        # if None: 
            # get the tweet history
        # else:
            # get the latest tweets
        # store the latest tweet_id




if __name__ == "__main__":

    monitor = Monitor()

    #while(true):


    # update user profiles
    monitor.check_twitter_seeds()


    # get latest user tweets
    



    # update user tweet store
    # for all tweets in user tweets:
        # add tweet to tweet queue
        # add any urls to entity queue

    # check all tweets for those that need updates
    # update tweets

    # check all entities for those that need updates
    # update entities