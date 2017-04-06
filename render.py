import config



es_data = config.es.search(index=config.AWS_ES_INDEX, body={"query": {"match": {"text": 'usa'}}}, size=600)
print(es_data)
