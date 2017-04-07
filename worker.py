import json
import config
import boto3
import string
import time
from watson_developer_cloud import AlchemyLanguageV1
from multiprocessing import Pool

#sqs = boto3.resource('sqs')
## queue = sqs.get_queue_by_name(QueueName = config.AWS_SQS_NAME)
#queue = sqs.Queue(url=config.AWS_SQS_URL)
sqs = boto3.resource('sqs',
    aws_access_key_id = config.AWS_ACCESS_KEY,
    aws_secret_access_key = config.AWS_SECRET_KEY
    )
queue = sqs.get_queue_by_name(QueueName = config.AWS_SQS_NAME)
sns = boto3.client('sns',
    aws_access_key_id = config.AWS_ACCESS_KEY,
    aws_secret_access_key = config.AWS_SECRET_KEY)
alchemy_language = AlchemyLanguageV1(api_key = config.Alchemy_Key)

def filter(raw_text):
    ans = ""
    for ch in range(len(raw_text)):
        if (0<=ord(raw_text[ch]) and ord(raw_text[ch])<=255):
            ans += raw_text[ch]
        else:
            continue
    return ans

def analyze_sentiment(queue):
	for message in queue.receive_messages():
		try:
			tweet = json.loads(message.body)
			if tweet is not None:
				clean_text = filter(tweet['text'])
				print (clean_text)
				analysis = json.loads(json.dumps(alchemy_language.sentiment(text = clean_text), indent = 2))
            	# print (tweet['text'])
				sentiment = analysis['docSentiment']['type']
				tweet['sentiment'] = sentiment
				tweet = json.dumps(tweet)
				# print ('New Tweet' + tweet)
				response = sns.publish( TopicArn = config.AWS_SNS_ARN,
										Message = str({'tweet': tweet})
									  )
				message.delete()
		except KeyboardInterrupt:
			break
		except Exception as e:
			print("Error: " + tweet['text'])
			message.delete()
			continue

if __name__ == '__main__':
    
	 pool = Pool(processes = 5)
	 while True:
	 	res = [pool.apply_async(analyze_sentiment(queue), ()) for i in range(5)]
	 	time.sleep(1)
#	while True:
#		analyze_sentiment(queue)
