
from db_cache import *
from queue import *


if __name__ == "__main__":

    cache = MongoDBCache(db='MediaMonitor')
    queue = Queue(cache)

    #while(true):
    
    # retrieve all users



    # check all users for those that need updates
    # update user profiles

    # get latest user tweets
    # update user tweet store
    # for all tweets in user tweets:
        # add tweet to tweet queue
        # add any urls to entity queue

    # check all tweets for those that need updates
    # update tweets

    # check all entities for those that need updates
    # update entities