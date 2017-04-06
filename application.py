from flask import Flask, render_template, request
import config
import json

application = Flask(__name__)

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

@application.route('/icon_result', methods = ['GET'])
def icon_result():
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
        return render_template("render.html", coords=json.dumps(coords))

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
