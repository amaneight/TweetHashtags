# Author: Aman Sehgal
# Title: Extract tweets from twitter for specific hashtags
#
# Date: 4/2/2018

#imports
import tweepy
import simplejson
import geocoder
import googlemaps

#Keys
consumer_key = "###########"
consumer_secret = "###########"
access_token = "###########"
access_secret = "###########"

# Set a hastag e.g github
hashtag = "#github" 

# Tweepy security setup
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# Own data strucutre to store tweets
tweet_data = {
            "type": "FeatureCollection",
            "features": []
        }
i = 0

# Iterate over retrieved tweets
try:
    for tweet in tweepy.Cursor(api.search,q=hashtag).items():
        i += 1
        tweet_dict = simplejson.loads(simplejson.dumps(tweet._json))

        # Extract relevant fields from tweet_dict
        tweet_json_feature = {
            "tweet_no": i,
            "text" : tweet_dict['text'],
            "favorite_count": tweet_dict['favorite_count'],
            "retweet_count": tweet_dict['retweet_count'],
            "source": tweet_dict['source'],
            "user_location": tweet.user.location,
            "place": tweet_dict['place'],
            "created_at": tweet_dict['created_at'],
        }

        # Store tweet in custom data structure
        tweet_data['features'].append(tweet_json_feature)

except tweepy.error.TweepError:
    print "Tweep error occurred"

finally:
	# Store tweets in json format
    with open('tweets.json', 'w') as fout:
        fout.write(simplejson.dumps(tweet_data, indent=4))
