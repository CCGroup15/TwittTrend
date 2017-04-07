import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import string
import json
import config
import boto3

#from http.client import IncompleteRead

sqs = boto3.resource('sqs',
                     aws_access_key_id = config.AWS_ACCESS_KEY,
                     aws_secret_access_key = config.AWS_SECRET_KEY);


def get_category(tweet):
    final_cat = []
    for category in config.FILTERS:
        if category in tweet:
            final_cat.append(category)
    return final_cat

class MyListener(StreamListener):
    def __init__(self):
        self.count = 0
        self.limit = 200
        # regularly stop the download process to avoid the "falling behind" error
    
    def on_data(self, data):
        try:
            if (self.count < self.limit):
                tweet = json.loads(data)
                if tweet['lang'] == 'en' and tweet['user'].get('location') is not None:
                    place = tweet['user'].get('location')
                    #print(place)
                    if place:
                        tweet_id = str(tweet['id'])
                        geocode_result = config.gmaps.geocode(place)
                        lat = geocode_result[0]['geometry']['location']['lat']
                        lng = geocode_result[0]['geometry']['location']['lng']
                        tweet_text = tweet['text'].lower().encode('ascii', 'ignore').decode('ascii')
                        raw_tweet = {
                            'id': tweet_id,
                            'user': tweet['user']['screen_name'],
                            'text': tweet_text,
                            'place': place,
                            'coordinates': {'location': str(lat)+","+str(lng)},
                            'time': tweet['created_at'],
                            'category': get_category(tweet_text)
                        }
                       # with open('result.json', 'a') as f:
                       #     f.write(json.dumps(raw_tweet))
                       
                        # send message to SQS
                        queue = sqs.get_queue_by_name(QueueName='MyQueue')
                        queue.send_message(MessageBody = json.dumps(raw_tweet));

                        # config.es.index(index = config.AWS_ES_INDEX, doc_type = config.AWS_ES_TYPE, id = tweet_id, body = raw_tweet)
                self.count += 1
            else:
                twitter_stream.disconnect()
        except Exception as e:
            print("Error on_data: %s" % str(e))
            # there is some uncomplete contents in tweets, we could output error messages to check

if __name__ == '__main__':
    while True:
        try:
            auth = OAuthHandler(config.consumer_key, config.consumer_secret)
            auth.set_access_token(config.access_token, config.access_secret)
            api = tweepy.API(auth)
            twitter_stream = Stream(auth, MyListener())
            twitter_stream.filter(track = config.FILTERS)
        except KeyboardInterrupt:
            break
        except:
            continue
            # IncompleteRead error occurs frequently, we directly restart the download process at that time

