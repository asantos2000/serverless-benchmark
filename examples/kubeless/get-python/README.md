# Deploy

```bash
anderson@mac-as:get-python$ kubeless function deploy get-python --runtime python2.7 \
>                                 --from-file test.py \
>                                 --handler test.foobar \
>                                 --trigger-http
INFO[0000] Deploying function...
INFO[0000] Function get-python submitted for deployment
INFO[0000] Check the deployment status executing 'kubeless function ls get-python'
```

# Verify

```bash
anderson@mac-as:get-python$ kubeless function ls get-python
NAME      	NAMESPACE	HANDLER    	RUNTIME  	TYPE	TOPIC	DEPENDENCIES	STATUS
get-python	default  	test.foobar	python2.7	HTTP	     	            	1/1 READY

anderson@mac-as:get-python$ kubectl get functions
NAME         AGE
get-python   6m

anderson@mac-as:get-python$ kubeless function ls
NAME      	NAMESPACE	HANDLER    	RUNTIME  	TYPE	TOPIC	DEPENDENCIES	STATUS
get-python	default  	test.foobar	python2.7	HTTP	     	            	1/1 READY
```

# Run

```bash
anderson@mac-as:get-python$ kubeless function call get-python --data '{"echo": "echo echo"}'
{"echo": "echo echo"}

anderson@mac-as:faas-netes(master)$ kubectl proxy -p 8080
Starting to serve on 127.0.0.1:8080 &

anderson@mac-as:get-python$ curl -L --data '{"Another": "Echo"}' localhost:8080/api/v1/proxy/namespaces/default/services/get-python:function-port/ --header "Content-Type:application/json"
{"Another": "Echo"}

# Needs ingress. See below
anderson@mac-as:get-python$ kubeless ingress list
+------+-----------+------+------+--------------+--------------+
| NAME | NAMESPACE | HOST | PATH | SERVICE NAME | SERVICE PORT |
+------+-----------+------+------+--------------+--------------+
+------+-----------+------+------+--------------+--------------+

anderson@mac-as:get-python$ kubeless ingress create route1 --function get-python

anderson@mac-as:get-python$ kubeless ingress list
+--------+-----------+----------------------------------+------+--------------+--------------+
|  NAME  | NAMESPACE |               HOST               | PATH | SERVICE NAME | SERVICE PORT |
+--------+-----------+----------------------------------+------+--------------+--------------+
| route1 | default   | get-python.192.168.99.100.nip.io | /    | get-python   |         8080 |
+--------+-----------+----------------------------------+------+--------------+--------------+

anderson@mac-as:get-python$ kubectl get ing
NAME      HOSTS                              ADDRESS   PORTS     AGE
route1    get-python.192.168.99.100.nip.io             80        46s

# Running
anderson@mac-as:get-python$ curl --data '{"Another": "Echo"}' --header "Host: get-python.192.168.99.100.nip.io" 192.168.99.100/ --header "Content-Type:application/json"
{"Another": "Echo"}

```

## Install ingress

Ref: [Add route to Kubeless function](https://github.com/kubeless/kubeless/blob/master/docs/routing.md#add-route-to-kubeless-function)

```bash
anderson@mac-as:get-python$ kubectl apply -f https://raw.githubusercontent.com/kubeless/kubeless/master/manifests/ingress/ingress-controller-http-only.yaml
replicationcontroller "default-http-backend" created
service "default-http-backend" created
replicationcontroller "nginx-ingress-controller" created
```

```bash
anderson@mac-as:get-python$ kubectl get pods -n default
NAME                             READY     STATUS    RESTARTS   AGE
default-http-backend-tw7wc       1/1       Running   0          5m
get-python-796bbdd98f-jknm8      1/1       Running   0          55s
nginx-ingress-controller-7xn84   1/1       Running   0          5m
```

**File:** ingress-controller-http-only.yaml

```yaml
# https://github.com/kubernetes/contrib/blob/master/ingress/controllers/nginx/examples/default-backend.yaml
apiVersion: v1
kind: ReplicationController
metadata:
  name: default-http-backend
spec:
  replicas: 1
  selector:
    app: default-http-backend
  template:
    metadata:
      labels:
        app: default-http-backend
    spec:
      terminationGracePeriodSeconds: 60
      containers:
      - name: default-http-backend
        # Any image is permissable as long as:
        # 1. It serves a 404 page at /
        # 2. It serves 200 on a /healthz endpoint
        image: gcr.io/google_containers/defaultbackend:1.0
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 30
          timeoutSeconds: 5
        ports:
        - containerPort: 8080
        resources:
          limits:
            cpu: 10m
            memory: 20Mi
          requests:
            cpu: 10m
            memory: 20Mi
---
# create a service for the default backend
apiVersion: v1
kind: Service
metadata:
  labels:
    app: default-http-backend
  name: default-http-backend
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 8080
  selector:
    app: default-http-backend
  sessionAffinity: None
  type: ClusterIP
---
# Replication controller for the load balancer
apiVersion: v1
kind: ReplicationController
metadata:
  name: nginx-ingress-controller
  labels:
    k8s-app: nginx-ingress-lb
spec:
  replicas: 1
  selector:
    k8s-app: nginx-ingress-lb
  template:
    metadata:
      labels:
        k8s-app: nginx-ingress-lb
        name: nginx-ingress-lb
    spec:
      terminationGracePeriodSeconds: 60
      containers:
      - image: gcr.io/google_containers/nginx-ingress-controller:0.8.2
        name: nginx-ingress-lb
        imagePullPolicy: Always
        livenessProbe:
          httpGet:
            path: /healthz
            port: 10249
            scheme: HTTP
          initialDelaySeconds: 30
          timeoutSeconds: 5
        # use downward API
        env:
          - name: POD_NAME
            valueFrom:
              fieldRef:
                fieldPath: metadata.name
          - name: POD_NAMESPACE
            valueFrom:
              fieldRef:
                fieldPath: metadata.namespace
        ports:
        - containerPort: 80
          hostPort: 80
        args:
        - /nginx-ingress-controller
        - --default-backend-service=default/default-http-backend
```
