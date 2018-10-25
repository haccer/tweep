## TODO - Fix Weekday situation
from elasticsearch import Elasticsearch, helpers
from time import strftime, localtime
import contextlib
import sys

class RecycleObject(object):
    def write(self, junk): pass
    def flush(self): pass

@contextlib.contextmanager
def nostdout():
    savestdout = sys.stdout
    sys.stdout = RecycleObject()
    yield
    sys.stdout = savestdout

def weekday(day):
    weekdays = {
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5,
            "Saturday": 6,
            "Sunday": 7,
            }

    return weekdays[day]

def hour(datetime):
    return strftime("%H", localtime(datetime))

def Tweet(Tweet, config):
    weekdays = {
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5,
            "Saturday": 6,
            "Sunday": 7,
            }
    day = weekdays[strftime("%A", localtime(Tweet.datetime))]

    actions = []
    nLikes = 1
    nReplies = 1
    nRetweets = 1

    dt = f"{Tweet.datestamp} {Tweet.timestamp}"

    j_data = {
            "_index": config.Index_tweets,
            "_type": config.Index_type,
            "_id": str(Tweet.id) + "_raw_" + config.Essid,
            "_source": {
                "id": str(Tweet.id),
                "conversation_id": Tweet.conversation_id,
                "created_at": Tweet.datetime,
                "date": dt,
                "timezone": Tweet.timezone,
                "place": Tweet.place,
                "location": Tweet.location,
                "tweet": Tweet.tweet,
                "hashtags": Tweet.hashtags,
                "user_id": Tweet.user_id,
                "user_id_str": Tweet.user_id_str,
                "username": Tweet.username,
                "name": Tweet.name,
                "profile_image_url": Tweet.profile_image_url,
                "day": day,
                "hour": hour(Tweet.datetime),
                "link": Tweet.link,
                "gif_url": Tweet.gif_url,
                "gif_thumb": Tweet.gif_thumb,
                "video_url": Tweet.video_url,
                "video_thumb": Tweet.video_thumb,
                "is_reply_to": Tweet.is_reply_to,
                "has_parent_tweet": Tweet.has_parent_tweet,
                "retweet": Tweet.retweet,
                "essid": config.Essid,
                "nlikes": int(Tweet.likes_count),
                "nreplies": int(Tweet.replies_count),
                "nretweets": int(Tweet.retweets_count),
                "is_quote_status": Tweet.is_quote_status,
                "quote_id": Tweet.quote_id,
                "quote_id_str": Tweet.quote_id_str,
                "quote_url": Tweet.quote_url,
                "search": str(config.Search)
                }
            }
    actions.append(j_data)

    if config.ES_count["likes"]:
        for l in range(int(Tweet.likes)):
            j_data = {
                    "_index": config.Index_tweets,
                    "_type": config.Index_type,
                    "_id": str(Tweet.id) + "_like_" + str(nLikes) + config.Essid,
                    "_source": {
                        "id": str(Tweet.id),
                        "conversation_id": Tweet.conversation_id,
                        "created_at": Tweet.datetime,
                        "date": dt,
                        "timezone": Tweet.timezone,
                        "place": Tweet.place,
                        "location": Tweet.location,
                        "tweet": Tweet.tweet,
                        "hashtags": Tweet.hashtags,
                        "user_id": Tweet.user_id,
                        "user_id_str": Tweet.user_id_str,
                        "username": Tweet.username,
                        "name": Tweet.name,
                        "profile_image_url": Tweet.profile_image_url,
                        "day": day,
                        "hour": hour(Tweet.datetime),
                        "link": Tweet.link,
                        "gif_url": Tweet.gif_url,
                        "gif_thumb": Tweet.gif_thumb,
                        "video_url": Tweet.video_url,
                        "video_thumb": Tweet.video_thumb,
                        "is_reply_to": Tweet.is_reply_to,
                        "has_parent_tweet": Tweet.has_parent_tweet,
                        "retweet": Tweet.retweet,
                        "essid": config.Essid,
                        "nlikes": int(Tweet.likes_count),
                        "nreplies": int(Tweet.replies_count),
                        "nretweets": int(Tweet.retweets_count),
                        "is_quote_status": Tweet.is_quote_status,
                        "quote_id": Tweet.quote_id,
                        "quote_id_str": Tweet.quote_id_str,
                        "quote_url": Tweet.quote_url,
                        "search": str(config.Search),
                        "likes": True
                        }
                    }
            actions.append(j_data)
            nLikes += 1

    if config.ES_count["replies"]:
        for rep in range(int(Tweet.replies)):
            j_data = {
                    "_index": config.Index_tweets,
                    "_type": config.Index_type,
                    "_id": str(Tweet.id) + "_reply_" + str(nReplies) + config.Essid,
                    "_source": {
                        "id": str(Tweet.id),
                        "conversation_id": Tweet.conversation_id,
                        "created_at": Tweet.datetime,
                        "date": dt,
                        "timezone": Tweet.timezone,
                        "place": Tweet.place,
                        "location": Tweet.location,
                        "tweet": Tweet.tweet,
                        "hashtags": Tweet.hashtags,
                        "user_id": Tweet.user_id,
                        "user_id_str": Tweet.user_id_str,
                        "username": Tweet.username,
                        "name": Tweet.name,
                        "profile_image_url": Tweet.profile_image_url,
                        "day": day,
                        "hour": hour(Tweet.datetime),
                        "link": Tweet.link,
                        "gif_url": Tweet.gif_url,
                        "gif_thumb": Tweet.gif_thumb,
                        "video_url": Tweet.video_url,
                        "video_thumb": Tweet.video_thumb,
                        "is_reply_to": Tweet.is_reply_to,
                        "has_parent_tweet": Tweet.has_parent_tweet,
                        "retweet": Tweet.retweet,
                        "essid": config.Essid,
                        "nlikes": int(Tweet.likes_count),
                        "nreplies": int(Tweet.replies_count),
                        "nretweets": int(Tweet.retweets_count),
                        "is_quote_status": Tweet.is_quote_status,
                        "quote_id": Tweet.quote_id,
                        "quote_id_str": Tweet.quote_id_str,
                        "quote_url": Tweet.quote_url,
                        "search": str(config.Search),
                        "replies": True
                        }
                    }
            actions.append(j_data)
            nReplies += 1

    if config.ES_count["retweets"]:
        for ret in range(int(Tweet.retweets)):
            j_data = {
                    "_index": config.Index_tweets,
                    "_type": config.Index_type,
                    "_id": str(Tweet.id) + "_retweet_" + str(nRetweets) + config.Essid,
                    "_source": {
                        "id": str(Tweet.id),
                        "conversation_id": Tweet.conversation_id,
                        "created_at": Tweet.datetime,
                        "date": dt,
                        "timezone": Tweet.timezone,
                        "place": Tweet.place,
                        "location": Tweet.location,
                        "tweet": Tweet.tweet,
                        "hashtags": Tweet.hashtags,
                        "user_id": Tweet.user_id,
                        "user_id_str": Tweet.user_id_str,
                        "username": Tweet.username,
                        "name": Tweet.name,
                        "profile_image_url": Tweet.profile_image_url,
                        "day": day,
                        "hour": hour(Tweet.datetime),
                        "link": Tweet.link,
                        "gif_url": Tweet.gif_url,
                        "gif_thumb": Tweet.gif_thumb,
                        "video_url": Tweet.video_url,
                        "video_thumb": Tweet.video_thumb,
                        "is_reply_to": Tweet.is_reply_to,
                        "has_parent_tweet": Tweet.has_parent_tweet,
                        "retweet": Tweet.retweet,
                        "essid": config.Essid,
                        "nlikes": int(Tweet.likes_count),
                        "nreplies": int(Tweet.replies_count),
                        "nretweets": int(Tweet.retweets_count),
                        "is_quote_status": Tweet.is_quote_status,
                        "quote_id": Tweet.quote_id,
                        "quote_id_str": Tweet.quote_id_str,
                        "quote_url": Tweet.quote_url,
                        "search": str(config.Search),
                        "retweets": True
                        }
                    }
            actions.append(j_data)
            nRetweets += 1

    es = Elasticsearch(config.Elasticsearch)
    with nostdout():
        helpers.bulk(es, actions, chunk_size=2000, request_timeout=200)
    actions = []

def Follow(user, config):
    actions = []

    j_data = {
            "_index": config.Index_follow,
            "_type": config.Index_type,
            "_id": user + "_" + config.Username + "_" + config.Essid,
            "_source": {
                "user": user,
                "follow": config.Username,
                "essid": config.Essid
                }
            }
    actions.append(j_data)

    es = Elasticsearch(config.Elasticsearch)
    with nostdout():
        helpers.bulk(es, actions, chunk_size=2000, request_timeout=200)
    actions = []

def UserProfile(user, config):
    actions = []

    j_data = {
            "_index": config.Index_users,
            "_type": config.Index_type,
            "_id": user.id + "_" + user.join_date + "_" + user.join_time + "_" + config.Essid,
            "_source": {
                "id": user.id,
                "name": user.name,
                "username": user.username,
                "bio": user.bio,
                "location": user.location,
                "url": user.url,
                "join_datetime": user.join_date + " " + user.join_time,
                "join_date": user.join_date,
                "join_time": user.join_time,
                "tweets": user.tweets,
                "following": user.following,
                "followers": user.followers,
                "likes": user.likes,
                "media": user.media_count,
                "private": user.is_private,
                "verified": user.is_verified,
                "avatar": user.avatar,
                "background_image": user.background_image,
                "session": config.Essid
                }
            }
    actions.append(j_data)

    es = Elasticsearch(config.Elasticsearch)
    with nostdout():
        helpers.bulk(es, actions, chunk_size=2000, request_timeout=200)
    actions = []