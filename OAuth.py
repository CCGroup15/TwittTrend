import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

# Access the data
consumer_key = 'k20CumsFv7l5JO0KqVIT03DeL'
consumer_secret = 'V57rHUlKcijBPzU6GlyYKNPQzjwM7bJEOmdKlTfWNEixh0y4er'
access_token = '4604284034-ZlWxWhxT9UTtNX42SmehU63XoA7ZsUGtyWxBWfn'
access_secret = 'HNbiT0w6UWiNxmhiGPhEI5xDR3kEKkGyswVmNSwTDA9ot'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
