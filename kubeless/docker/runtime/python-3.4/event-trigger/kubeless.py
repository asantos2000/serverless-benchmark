#!/usr/bin/env python

import sys
import traceback
import os
import imp
import json

from multiprocessing import Process, Queue
from kafka import KafkaConsumer
import prometheus_client as prom

mod_name = os.getenv('MOD_NAME')
func_handler = os.getenv('FUNC_HANDLER')
topic_name = os.getenv('TOPIC_NAME')
timeout = float(os.getenv('FUNC_TIMEOUT', 180))

group = mod_name + func_handler

if "KUBELESS_KAFKA_SVC" in os.environ:
    kafka_svc = os.getenv('KUBELESS_KAFKA_SVC')
else:
    kafka_svc = 'kafka'

if "KUBELESS_KAFKA_NAMESPACE" in os.environ:
    kafka_namespace = os.getenv('KUBELESS_KAFKA_NAMESPACE')
else:
    kafka_namespace = 'kubeless'

kafka_server = '%s.%s:9092' % (kafka_svc, kafka_namespace)

mod = imp.load_source('function', '/kubeless/%s.py' % mod_name)
func = getattr(mod, func_handler)

func_hist = prom.Histogram('function_duration_seconds',
                           'Duration of user function in seconds',
                           ['topic'])
func_calls = prom.Counter('function_calls_total',
                           'Number of calls to user function',
                          ['topic'])
func_errors = prom.Counter('function_failures_total',
                           'Number of exceptions in user function',
                           ['topic'])

def funcWrap(q, payload):
    q.put(func(payload))

def json_safe_loads(msg):
    try:
        data = json.loads(msg)
        return {'type': 'json', 'payload': data}
    except:
        return {'type': 'text', 'payload': msg}

consumer = KafkaConsumer(
    bootstrap_servers=kafka_server,
    group_id=group, value_deserializer=json_safe_loads)
consumer.subscribe([topic_name])

def handle(msg):
    func_calls.labels(topic_name).inc()
    with func_errors.labels(topic_name).count_exceptions():
        with func_hist.labels(topic_name).time():
            q = Queue()
            p = Process(target=funcWrap, args=(q,msg.value['payload'],))
            p.start()
            p.join(timeout)
            # If thread is still active
            if p.is_alive():
                p.terminate()
                p.join()
                raise Exception('Timeout while processing the function')
            else:
                return q.get()

if __name__ == '__main__':
    prom.start_http_server(8080)

    while True:
        for msg in consumer:
            try:
                res = handle(msg)
                sys.stdout.write(str(res) + '\n')
                sys.stdout.flush()

            except Exception:
                traceback.print_exc()
