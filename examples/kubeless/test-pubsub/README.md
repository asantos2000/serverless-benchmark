# Deploy

```bash
anderson@mac-as:test-pubsub$ kubeless function deploy test --runtime python2.7 \
>                                 --handler test.foobar \
>                                 --from-file test.py \
>                                 --trigger-topic test-topic
INFO[0000] Deploying function...
INFO[0000] Function test submitted for deployment
INFO[0000] Check the deployment status executing 'kubeless function ls test'
```

# Verify

```bash
anderson@mac-as:test-pubsub$ kubeless function ls
NAME      	NAMESPACE	HANDLER    	RUNTIME  	TYPE  	TOPIC     	DEPENDENCIES	STATUS
get-python	default  	test.foobar	python2.7	HTTP  	          	            	1/1 READY
test      	default  	test.foobar	python2.7	PubSub	test-topic	            	1/1 READY

```

# RUN

```bash
anderson@mac-as:test-pubsub$ kubeless topic list
__consumer_offsets
test-topic

anderson@mac-as:test-pubsub$ kubeless topic publish --topic test-topic --data "Hello World"

anderson@mac-as:test-pubsub$ kubectl get pods
NAME                             READY     STATUS    RESTARTS   AGE
default-http-backend-tw7wc       1/1       Running   0          21m
get-python-796bbdd98f-tz78d      1/1       Running   0          4m
nginx-ingress-controller-7xn84   1/1       Running   0          21m
test-6bdd59c67b-szh77            1/1       Running   0          4m   <------

anderson@mac-as:test-pubsub$ kubectl logs test-6bdd59c67b-szh77
Hello World
```

# Nota
Os PODs criados são reiniciados a cada 5min (5:23) sem motivo aparente.

```bash
$ while true;do kubectl get pods; sleep 1; echo "---"; done
```