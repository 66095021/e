#!/usr/bin/env python
import threading, logging, time

from kafka import KafkaConsumer, KafkaProducer


from elasticsearch import Elasticsearch
from elasticsearch import helpers
es = Elasticsearch()

id_v=0

def send_to_es(value):
	global id_v
	a={}
	a["_index"]="bro"
	a["_type"]="dns"
	id_v=id_v+1
	a["_id"]=id_v
	a["doc"]=value
	data=[]
	data.append(a)
	helpers.bulk(es, data)


class Consumer(threading.Thread):
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 auto_offset_reset='earliest')
        consumer.subscribe(['bro'])

	while True:

	        for message in consumer:
        	    print message.value
		    send_to_es(message.value)

def main():
    threads = [
        Consumer()
    ]

    for t in threads:
        t.start()

    time.sleep(10)

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
    main()
