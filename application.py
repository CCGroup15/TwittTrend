from flask import Flask, render_template, request, Response
import config
import string
import json

application = Flask(__name__)

@application.route('/send', methods=["POST"])
def insert_es():
    data = request.data
    data = data.decode("utf-8")
    print(data)
    message = json.loads(data)
    if message['Type'] == "SubscriptionConfirmation" :
    	print("!!!!!!" + message['SubscribeURL'] + "!!!!!!")
    else :
    	#tweet = message['Message']
        #config.es.index(index = config.AWS_ES_INDEX, doc_type = config.AWS_ES_TYPE, id = tweet['id'], body = tweet)
        config.es.index(index=config.AWS_ES_INDEX, doc_type=config.AWS_ES_TYPE, body=message['Message'])


    return Response(json.dumps('{"state":"success"}'), content_type = 'application/json')

@application.route('/')
def say_hello():
    category = config.FILTERS
    coords = []
    for keyword in category:
        es_data = config.es.search(index=config.AWS_ES_INDEX, body={"query": {"match": {"text": keyword}}}, size=600)
        for data in es_data['hits']['hits']:
            if len(data['_source']['coordinates']) > 0:
                geo_data = data['_source']['coordinates']['location'].split(',')
                lat = float(geo_data[0])
                lng = float(geo_data[1])
                coords.append([lat, lng])
    return render_template("render.html", coords=json.dumps(coords))
    # return render_template("render.html")


@application.route('/icon_result/<category>', methods = ['GET'])
def icon_result(category):
    if request.method == 'GET':
        # category = request.args.getlist("category")
        #coords = []
        tweet_sent = []
        target_word = []
        if category=='all' or category=='undefined':
            target_word = config.FILTERS
        else:
            #es_data = config.es.search(index=config.AWS_ES_INDEX, body={"query": {"match": {"text": category}}}, size=600)
        	target_word.append(category)
        # print(es_data)
        for keyword in target_word:
        	es_data = config.es.search(index=config.AWS_ES_INDEX, body={"query": {"match": {"text": keyword}}}, size=600)
        	for data in es_data['hits']['hits']:
        		if (len(data['_source']['coordinates']) > 0):
        			geo_data = data['_source']['coordinates']['location'].split(',')
        			lat = float(geo_data[0])
        			lng = float(geo_data[1])
        			senti_txt = data['_source']['sentiment']
        			if (senti_txt=='negative'):
        				senti = -1
        			elif (senti_txt=='positive'):
        				senti = 1
        			else:
        				senti = 0
        			res = {"coordinates" : [lat,lng, senti] }
        			tweet_sent.append(res)
    return Response(json.dumps(tweet_sent), content_type= 'application/json')

@application.route('/heat_hello')
def heat_hello():
    category = config.FILTERS
    coords = []
    for keyword in category:
        es_data = config.es.search(index=config.AWS_ES_INDEX, body={"query": {"match": {"text": keyword}}}, size=600)
        for data in es_data['hits']['hits']:
            if len(data['_source']['coordinates']) > 0:
                geo_data = data['_source']['coordinates']['location'].split(',')
                lat = float(geo_data[0])
                lng = float(geo_data[1])
                coords.append([lat, lng])
    return render_template("heat_render.html", coords=json.dumps(coords))

@application.route('/heat_result', methods = ['GET'])
def heat_result():
    if request.method == 'GET':
        category = request.args.getlist("category")
        # print(category)
        coords = []
        for keyword in category:
            es_data = config.es.search(index=config.AWS_ES_INDEX, body={"query": {"match": {"text": keyword}}}, size=600)
            # print(es_data)
            for data in es_data['hits']['hits']:
                if len(data['_source']['coordinates']) > 0:
                    geo_data = data['_source']['coordinates']['location'].split(',')
                    lat = float(geo_data[0])
                    lng = float(geo_data[1])
                    coords.append([lat, lng])
        # print(coords)
        return render_template("heat_render.html", coords=json.dumps(coords))

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
