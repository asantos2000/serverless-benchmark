# Serverless with fnproject.io
The Fn project is a container native serverless platform that you can run anywhere -- any cloud or on-premise. It’s easy to use, supports every programming language, and is extensible and performant.

Alternatives: http://fission.io

## Developmen enviroment

### Install container

1. [Docker](https://docs.docker.com/engine/installation/)
2. Optional: [Fn Project Helm Chart](https://medium.com/fnproject/fn-project-helm-chart-for-kubernetes-e97ded6f4f0c)

> If you're using virtualbox (option 2), and ypu're having problems to access your services, it'll necessary configure virtualbox's network port fowarding and map localhost ports to service ports.

### Install fn client

![user input](images/terminal64.png)

```bash
$ curl -LSs https://raw.githubusercontent.com/fnproject/cli/master/install | sh
```

### Deploying first example

![user input](images/terminal64.png)

```bash
$ mkdir first-example
```

```bash
$ fn init --runtime java
        ______
       / ____/___
      / /_  / __ \
     / __/ / / / /
    /_/   /_/ /_/

Runtime: java
Function boilerplate generated.
func.yaml created.
```

```bash
$ fn run
Building image first-example:0.0.1
Sending build context to Docker daemon  13.82kB
Step 1/11 : FROM fnproject/fn-java-fdk-build:jdk9-latest as build-stage
 ---> 4f9ffea5cc37
Step 2/11 : WORKDIR /function
 ---> Using cache
 ---> f7f40fd849b6
Step 3/11 : ENV MAVEN_OPTS -Dhttp.proxyHost= -Dhttp.proxyPort= -Dhttps.proxyHost= -Dhttps.proxyPort= -Dhttp.nonProxyHosts= -Dmaven.repo.local=/usr/share/maven/ref/repository
 ---> Using cache
 ---> 1381ac584c6e
Step 4/11 : ADD pom.xml /function/pom.xml
 ---> Using cache
 ---> 17bd932f0bb3
Step 5/11 : RUN mvn package dependency:copy-dependencies -DincludeScope=runtime -DskipTests=true -Dmdep.prependGroupId=true -DoutputDirectory=target --fail-never
 ---> Using cache
 ---> a03c29dd9a2a
Step 6/11 : ADD src /function/src
 ---> Using cache
 ---> 3da6167d03a9
Step 7/11 : RUN mvn package
 ---> Using cache
 ---> d9764b7225a7
Step 8/11 : FROM fnproject/fn-java-fdk:jdk9-latest
 ---> d2027594962d
Step 9/11 : WORKDIR /function
 ---> Using cache
 ---> bb9f694c064d
Step 10/11 : COPY --from=build-stage /function/target/*.jar /function/app/
 ---> Using cache
 ---> 9e501c5a20b6
Step 11/11 : CMD com.example.fn.HelloFunction::handleRequest
 ---> Using cache
 ---> 16640cbbab27
Successfully built 16640cbbab27
Successfully tagged first-example:0.0.1
Hello, world!
```

```bash
$ docker images
REPOSITORY                    TAG                 IMAGE ID            CREATED             SIZE
first-example                 0.0.1               16640cbbab27        27 minutes ago      393MB
fnproject/fn-java-fdk         jdk9-latest         d2027594962d        21 hours ago        393MB
fnproject/fn-java-fdk-build   jdk9-latest         4f9ffea5cc37        21 hours ago        408MB
```

```bash
$ fn start
mount: permission denied (are you root?)
Could not mount /sys/kernel/security.
AppArmor detection and --privileged mode might break.
mount: permission denied (are you root?)
time="2017-12-01T13:21:58Z" level=info msg="datastore dialed" datastore=sqlite3 max_idle_connections=256
time="2017-12-01T13:21:58Z" level=info msg="started tracer" url=
time="2017-12-01T13:21:58Z" level=info msg="no docker auths from config files found (this is fine)" error="open /root/.dockercfg: no such file or directory"
time="2017-12-01T13:21:58Z" level=info msg="available memory" ram=7807500288
time="2017-12-01T13:21:58Z" level=info msg="Serving Functions API on address `:8080`"

        ______
       / ____/___
      / /_  / __ \
     / __/ / / / /
    /_/   /_/ /_/
        v0.3.209
        
$ fn apps list
```

```bash
$ fn deploy --app hello-java --local

Deploying first-example to app: hello-java at path: /first-example
Bumped to version 0.0.2
Building image first-example:0.0.2
Sending build context to Docker daemon  93.18kB
Step 1/11 : FROM fnproject/fn-java-fdk-build:jdk9-latest as build-stage
 ---> 4f9ffea5cc37
Step 2/11 : WORKDIR /function
 ---> d4dfee1376e9
Removing intermediate container e4bbd656d65b
Step 3/11 : ENV MAVEN_OPTS -Dhttp.proxyHost= -Dhttp.proxyPort= -Dhttps.proxyHost= -Dhttps.proxyPort= -Dhttp.nonProxyHosts= -Dmaven.repo.local=/usr/share/maven/ref/repository
 ---> Running in 260b6784f354
 ---> b9e6bf4d2f34
Removing intermediate container 260b6784f354
Step 4/11 : ADD pom.xml /function/pom.xml

...

[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 6.805 s
[INFO] Finished at: 2017-12-01T13:34:53Z
[INFO] Final Memory: 14M/47M
[INFO] ------------------------------------------------------------------------
 ---> 7d2ac91469a6
Removing intermediate container c12758d3baee
Step 8/11 : FROM fnproject/fn-java-fdk:jdk9-latest
 ---> d2027594962d
Step 9/11 : WORKDIR /function
 ---> Using cache
 ---> bb9f694c064d
Step 10/11 : COPY --from=build-stage /function/target/*.jar /function/app/
 ---> 507d5dc19e8c
Step 11/11 : CMD com.example.fn.HelloFunction::handleRequest
 ---> Running in 329a1ff503ac
 ---> 204666855e71
Removing intermediate container 329a1ff503ac
Successfully built 204666855e71
Successfully tagged first-example:0.0.2
Updating route /first-example using image first-example:0.0.2...
```

#### Start FN dashboard

![user input](images/terminal64.png)

```bash

$ docker ps
CONTAINER ID        IMAGE                 COMMAND                  CREATED                  STATUS              PORTS                              NAMES
d9376791717f        fnproject/functions   "preentry.sh ./fun..."   Less than a second ago   Up 8 seconds        2375/tcp, 0.0.0.0:8080->8080/tcp   functions

$ docker run --rm -it --link functions -p 4000:4000 -e "FN_API_URL=http://api:8080" fnproject/ui

> FunctionsUI@0.0.21 start /app
> node server

Using API url: api:8080
Server running on port 4000
GET http://api:8080/v1/apps, params:  {}
GET http://api:8080/stats, params:  {}
mac-as:~$ docker run --rm -it --link functions -p 4000:4000 -e "FN_API_URL=http://api:8080" fnproject/ui
```

#### Calling your function

**Local**

![user input](images/terminal64.png)

```bash
echo -n Anderson | fn run
Hello, Anderson!
```

**Remote**

![user input](images/terminal64.png)

```bash
$ echo -n Anderson | fn call hello-java first-example
Hello, Anderson!

$ curl -X POST -d 'Anderson' http://localhost:8080/r/hello-java/first-example
Hello, Anderson!
```

Open your browser at http://localhost:4000 and go to your app (hello-java) and run your function.

## Create an app

Fn supports grouping functions into a set that defines an application (or API), making it easy to organize and deploy.

This part is easy, just create an `app.yaml` file and put a name in it:

![user input](images/terminal64.png)

```sh
$ mkdir myapp2
$ cd myapp2
$ echo 'name: myapp2' > app.yaml
```

This directory will be the root of your application.

### Create a root function

The root function will be available at `/` on your application.

![user input](images/terminal64.png)

```sh
$ fn init --runtime ruby
```

Now we have a Ruby function alongside our `app.yaml`.

### Create a sub route

Now let's create a sub route at `/hello`:

![user input](images/terminal64.png)

```sh
$ fn init --runtime go hello
```

Now we have two functions in our app. Run:

![user input](images/terminal64.png)

```sh
$ ls
```

To see our root function, our `app.yaml` and a directory named `hello`.

### Deploy the entire app

Now we can deploy the entire application with one command:

![user input](images/terminal64.png)

```sh
$ fn deploy --all --local
```

Once the command is done, let's surf to our application:

* Root function at: http://localhost:8080/r/myapp2/
* And the hello function at: http://localhost:8080/r/myapp2/hello

### Wrapping Up

Congratulations! In this tutorial you learned how to group functions into an application and deploy them
with a single command.


## Cluster enviroment

1. [Install kuberentes-helm](https://github.com/kubernetes/helm)
1. Update permissions for fnProject
1. Customize chart for non-cloud enviroment
1. [Install chart](https://github.com/fnproject/fn-helm)

### 2. Update permission for fnProject

```bash
$ vi fnproject-rbac.yaml
```

```yaml
# NOTE: The service account `default:default` already exists in k8s cluster.
# You can create a new account following like this:
#---
#apiVersion: v1
#kind: ServiceAccount
#metadata:
#  name: <new-account-name>
#  namespace: <namespace>

---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: fnproject-rbac
subjects:
  - kind: ServiceAccount
    # Reference to upper's `metadata.name`
    name: default
    # Reference to upper's `metadata.namespace`
    namespace: default
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
```

```bash
kubectl apply -f fnproject-rbac.yaml
```

> Set permission for fnlb get pods

### 3. Customize chart for non-cloud enviroment

> You'll download this file from git in the next step.
> 
> Change this file before execute helm install.
> 
> Choose diferent name from my-release for your release (ex: vivp-poc).

**fn-helm/fn/values.yaml**

```yaml
# Default values for Fn
imagePullPolicy: IfNotPresent

fn:
  service:
    port: 80
    type: NodePort
    annotations: {}

fnlb:
  image: fnproject/fnlb:0.0.189

fnserver:
  image: fnproject/fnserver:0.3.227  #TAG-fnserver-image
  logLevel: info
  resources: {}
  nodeSelector: {}
  tolerations: []


ui:
  enabled: true
  fnui:
    image: fnproject/ui:0.0.21  #TAG-fnui-image
    resources: {}
  flowui:
    image: fnproject/flow:ui #TAG-flowui-image
    resources: {}
  service:
    flowuiPort: 3000
    fnuiPort: 4000
    type: NodePort
    annotations: {}


flow:
  image: fnproject/flow:0.1.75  #TAG-flow-image
  logLevel: info
  service:
    port: 81
    type: NodePort
    annotations: {}
  resources: {}


##
## MySQL chart configuration
##
mysql:
  persistence:
    enabled: false
    nodeSelector: mysql-storage
    ## If defined, volume.beta.kubernetes.io/storage-class: <storageClass>
    ## Default: volume.alpha.kubernetes.io/storage-class: default
    ##
    # storageClass:
    storageClass: mysql
    accessMode: ReadWriteOnce
    size: 8Gi

  mysqlDatabase: fndb
  mysqlUser: fnapp
  mysqlPassword: boomsauce

##
## Redis chart configuration
##
redis:
  persistence:
    enabled: false
    nodeSelector: redis-storage
    storageClass: redis
    accessMode: ReadWriteOnce
    size: 8Gi
  usePassword: false

## Ingress configuration.
## ref: https://kubernetes.io/docs/user-guide/ingress/
##
ingress:
  enabled: false
```

#### Installing on selected cluster

```bash
$ kubectl config current-context # to change use use-context <context>
minikube

$ cd fn-helm

$ helm install --name vivo-poc fn
LAST DEPLOYED: Wed Jan 10 10:53:28 2018
NAMESPACE: default
STATUS: DEPLOYED
..

$ helm status vivo-poc

anderson@mac-as:fn-helm(master)*$ helm status vivo-poc fn
LAST DEPLOYED: Wed Jan 10 10:53:28 2018
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1beta1/DaemonSet
NAME             DESIRED  CURRENT  READY  UP-TO-DATE  AVAILABLE  NODE SELECTOR  AGE
vivo-poc-fn-api  1        1        1      1           1          <none>         3m

==> v1beta1/Deployment
NAME                   DESIRED  CURRENT  UP-TO-DATE  AVAILABLE  AGE
vivo-poc-mysql         1        1        1           1          3m
vivo-poc-redis         1        1        1           1          3m
vivo-poc-fn-flow-depl  1        1        1           1          3m
vivo-poc-fn-fnlb-depl  1        1        1           1          3m
vivo-poc-fn-ui         1        1        1           1          3m

==> v1/Pod(related)
NAME                             READY  STATUS   RESTARTS  AGE
vivo-poc-fn-api-wl558            1/1    Running  1         3m
vivo-poc-mysql-57778577d4-sd5gx  1/1    Running  0         3m
vivo-poc-redis-75f66c5c5f-w6dlz  1/1    Running  0         3m

==> v1/Secret
NAME            TYPE    DATA  AGE
vivo-poc-mysql  Opaque  2     3m

==> v1/Service
NAME              TYPE       CLUSTER-IP      EXTERNAL-IP  PORT(S)                        AGE
vivo-poc-mysql    ClusterIP  10.102.226.143  <none>       3306/TCP                       3m
vivo-poc-redis    ClusterIP  10.103.177.104  <none>       6379/TCP                       3m
vivo-poc-fn-flow  NodePort   10.97.151.179   <none>       81:31908/TCP                   3m
vivo-poc-fn-api   NodePort   10.103.16.3     <none>       80:30822/TCP                   3m
vivo-poc-fn-ui    NodePort   10.97.219.90    <none>       3000:30728/TCP,4000:32151/TCP  3m


NOTES:
The Fn service can be accessed within your cluster at:

 - http://vivo-poc-fn-api.default:80

Set the FN_API_URL environment variable to this address to use the Fn service from outside the cluster:

    export NODE_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services vivo-poc-fn-api)
    export NODE_IP=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")

    export FN_API_URL=http://$NODE_IP:$NODE_PORT

############################################################################
###   WARNING: Persistence is disabled!!! You will lose function and     ###
###   flow state when the MySQL pod is terminated.                       ###
###   See the README.md for instructions on configuring persistence.     ###
############################################################################

``` 

### Locate fn-api port on cluster

#### First method

```bash
$ kubectl get services
anderson@mac-as:fn-helm(master)*$ kubectl get services
NAME               TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                         AGE
kubernetes         ClusterIP   10.96.0.1        <none>        443/TCP                         2d
vivo-poc-fn-api    NodePort    10.109.173.143   <none>        80:30021/TCP                    2h
vivo-poc-fn-flow   NodePort    10.100.170.207   <none>        81:31177/TCP                    2h
vivo-poc-fn-ui     NodePort    10.111.125.248   <none>        3000:31327/TCP,4000:30246/TCP   2h
vivo-poc-mysql     ClusterIP   10.111.78.103    <none>        3306/TCP                        2h
vivo-poc-redis     ClusterIP   10.107.207.124   <none>        6379/TCP                        2h
```

#### Second method

```bash
anderson@mac-as:fn-helm(master)*$ helm status vivo-poc

LAST DEPLOYED: Mon Jan  8 15:10:45 2018
NAMESPACE: default
STATUS: DEPLOYED
 
RESOURCES:
==> v1/Secret
NAME            TYPE    DATA  AGE
vivo-poc-mysql  Opaque  2     2h
 
==> v1/Service
NAME              TYPE       CLUSTER-IP      EXTERNAL-IP  PORT(S)                        AGE
vivo-poc-mysql    ClusterIP  10.111.78.103   <none>       3306/TCP                       2h
vivo-poc-redis    ClusterIP  10.107.207.124  <none>       6379/TCP                       2h
vivo-poc-fn-flow  NodePort   10.100.170.207  <none>       81:31177/TCP                   2h
vivo-poc-fn-api   NodePort   10.109.173.143  <none>       80:30021/TCP                   2h
vivo-poc-fn-ui    NodePort   10.111.125.248  <none>       3000:31327/TCP,4000:30246/TCP  2h
 
==> v1beta1/DaemonSet
NAME             DESIRED  CURRENT  READY  UP-TO-DATE  AVAILABLE  NODE SELECTOR  AGE
vivo-poc-fn-api  3        3        3      3           3          <none>         2h
 
==> v1beta1/Deployment
NAME                   DESIRED  CURRENT  UP-TO-DATE  AVAILABLE  AGE
vivo-poc-mysql         1        1        1           1          2h
vivo-poc-redis         1        1        1           1          2h
vivo-poc-fn-flow-depl  1        1        1           1          2h
vivo-poc-fn-fnlb-depl  1        1        1           1          2h
vivo-poc-fn-ui         1        1        1           1          2h
 
==> v1/Pod(related)
NAME                             READY  STATUS    RESTARTS  AGE
vivo-poc-fn-api-175f4            1/1    Running   4         2h
vivo-poc-fn-api-6j96w            1/1    Running   0         1h
vivo-poc-fn-api-p6978            1/1    Running   0         58m
vivo-poc-mysql-273033387-34nqb   0/1    Init:0/1  0         2h
vivo-poc-redis-2219699869-l0fvn  1/1    Running   0         2h
 
 
NOTES:
The Fn service can be accessed within your cluster at:
 
- http://vivo-poc-fn-api.default:80
 
Set the FN_API_URL environment variable to this address to use the Fn service from outside the cluster:
 
    export NODE_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services vivo-poc-fn-api)
    export NODE_IP=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
 
    export FN_API_URL=http://$NODE_IP:$NODE_PORT
 
############################################################################
###   WARNING: Persistence is disabled!!! You will lose function and     ###
###   flow state when the MySQL pod is terminated.                       ###
###   See the README.md for instructions on configuring persistence.     ###
############################################################################

```

### On your local computer 
```bash
anderson@mac-as:fn-helm(master)*$ export API_URL=export API_URL=http://10.100.18.10:30021

anderson@mac-as:fn-helm(master)*$ fn apps list
no apps found
```

## More examples

![user input](images/terminal64.png)

```bash
$ git clone https://github.com/asantos2000/serverless.git fn-examples
```

## References
1. [Fn Project home](https://fnproject.io/)
1. [Github - The container native, cloud agnostic serverless platform](https://github.com/fnproject/fn)
1. [Java API and runtime for fn](https://github.com/fnproject/fdk-java)
1. [CLI tool for fnproject](https://github.com/fnproject/cli)
1. [Serverless Architectures - Let's Ditch the Servers?](https://codeahoy.com/2016/06/25/serverless-architectures-lets-ditch-the-servers/)
1. [Database Connections in Lambda](http://blog.rowanudell.com/database-connections-in-lambda/)
1. [Best practices for Serverless: Connection Pooling your database](http://blog.spotinst.com/2017/11/19/best-practices-serverless-connection-pooling-database/)
1. [Top 10 JDBC Best Practices for Java Programmer](http://javarevisited.blogspot.com.br/2012/08/top-10-jdbc-best-practices-for-java.html)
1. [Best practices in Coding, Designing and Architecting Java Applications](https://github.com/in28minutes/java-best-practices#data-layer)
1. [Install Docker](https://docs.docker.com/engine/installation/)
