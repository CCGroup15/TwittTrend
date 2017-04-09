import json
import config
import boto3
import string
import time
from watson_developer_cloud import AlchemyLanguageV1
from multiprocessing import Pool, Lock
from kafka import KafkaConsumer

# sqs = boto3.resource('sqs')
# queue = sqs.get_queue_by_name(QueueName = config.AWS_SQS_NAME)
# queue = sqs.Queue(url=config.AWS_SQS_URL)
# sqs = boto3.resource('sqs',
#     aws_access_key_id = config.AWS_ACCESS_KEY,
#     aws_secret_access_key = config.AWS_SECRET_KEY
#     )
# queue = sqs.get_queue_by_name(QueueName = config.AWS_SQS_NAME)
sns = boto3.client('sns',
    aws_access_key_id = config.AWS_ACCESS_KEY,
    aws_secret_access_key = config.AWS_SECRET_KEY)
alchemy_language = AlchemyLanguageV1(api_key = config.Alchemy_Key)

lock = Lock()

def filter(raw_text):
    ans = ""
    for ch in range(len(raw_text)):
        if (0<=ord(raw_text[ch]) and ord(raw_text[ch])<=255):
            ans += raw_text[ch]
        else:
            continue
    return ans

def getFromKafka():
	lock.acquire()
	# print('getFromKafka')
	consumer_t = KafkaConsumer(config.KAFKA_TOPIC, bootstrap_servers=[config.KAFKA_HOST], enable_auto_commit=True)
	# print(consumer_t)
	for tweet_message in consumer_t:
		try:
			if tweet_message is None:
				continue
			print(tweet_message.value)
			tweet = json.loads(tweet_message.value.decode('utf-8'))
			if tweet is not None:
				clean_text = filter(tweet['text'])
				analysis = json.loads(json.dumps(alchemy_language.sentiment(text = clean_text), indent = 2))
				sentiment = analysis['docSentiment']['type']
				tweet['sentiment'] = sentiment
				tweet = json.dumps(tweet)
				response = sns.publish( TopicArn = config.AWS_SNS_ARN,
										Message = json.dumps({'default': tweet}),
                						MessageStructure='json'
										)
		except KeyboardInterrupt:
			break
		except Exception as e:
			print("Error: " + tweet['text'])
			continue

	lock.release()

if __name__ == '__main__':
	pool = Pool(processes = 3)
	while True:
		res = [pool.apply_async(getFromKafka(), ()) for i in range(3)]
		time.sleep(1)
