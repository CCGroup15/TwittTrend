import json
import config
import boto3
import string
import time
from watson_developer_cloud import AlchemyLanguageV1
from multiprocessing import Pool

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName = config.AWS_SQS_NAME)
sns = boto3.client('sns')
alchemy_language = AlchemyLanguageV1(api_key = config.Alchemy_Key)

def analyze_sentiment(queue):
	for message in queue.receive_messages():
		tweet = json.loads(message.body)
		if tweet is not None:
			analysis = json.loads(json.dumps(alchemy_language.sentiment(text = tweet['text']), indent = 2))
			# print tweet['text']
			sentiment = analysis['docSentiment']['type']
			tweet['sentiment'] = sentiment
			tweet = json.dumps(tweet)
			print 'New Tweet' + tweet

			response = sns.publish( TopicArn = config.AWS_SNS_ARN,
									Message = str({'default': tweet})
									)
			message.delete()

			# print(response)


if __name__ == '__main__':
	# pool = Pool(processes = 5)
	# while True:
	# 	res = [pool.apply_async(analyze_sentiment(queue), ()) for i in range(5)]
	# 	time.sleep(1)
	while True:
		analyze_sentiment(queue)
