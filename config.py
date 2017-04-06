from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import googlemaps

consumer_key = 'k20CumsFv7l5JO0KqVIT03DeL'
consumer_secret = 'V57rHUlKcijBPzU6GlyYKNPQzjwM7bJEOmdKlTfWNEixh0y4er'
access_token = '4604284034-ZlWxWhxT9UTtNX42SmehU63XoA7ZsUGtyWxBWfn'
access_secret = 'HNbiT0w6UWiNxmhiGPhEI5xDR3kEKkGyswVmNSwTDA9ot'


AWS_ACCESS_KEY="AKIAIL3NHK64XN6BNPMA"
AWS_SECRET_KEY="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"
AWS_REGION="us-east-1"

AWS_ES_PORT  = 443
AWS_ES_HOST = "search-twitter-map-sh6gbw33qb4r36en7ckqhvbdt4.us-east-1.es.amazonaws.com"
AWS_ES_INDEX = 'twitter-map'
AWS_ES_TYPE = 'tweet'

AWS_SQS_NAME = 'MyQueue'
AWS_SNS_ARN = 'arn:aws:sns:us-east-1:357531095488:tweet'

awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, 'es')

es = Elasticsearch(
    hosts=[{'host': AWS_ES_HOST, 'port': AWS_ES_PORT}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

GMAP_KEY = 'AIzaSyAovkBO68rNju_an3XHa29XmUQ0RWq55Is'
gmaps = googlemaps.Client(key=GMAP_KEY)


Alchemy_Key = '942dd1220a1e1ec17c0dd81c52a6b54dc7551800'
# Alchemy_Key = '4bb03d3d29aa773227a4f999f2842d6e04f6cf10'

FILTERS = ['china', 'usa', 'japan', 'russia', 'england', 'france', 'german']