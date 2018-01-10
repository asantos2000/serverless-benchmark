# Deploy

```bash
anderson@mac-as:find$ faas build -f ./find-python.yml
2018/01/10 17:33:54 No templates found in current directory.
2018/01/10 17:33:54 HTTP GET https://github.com/openfaas/faas-cli/archive/master.zip
2018/01/10 17:33:57 Writing 289Kb to master.zip

2018/01/10 17:33:57 Attempting to expand templates from master.zip
2018/01/10 17:33:58 Fetched 10 template(s) : [csharp go-armhf go node-arm64 node-armhf node python-armhf python python3 ruby] from https://github.com/openfaas/faas-cli
2018/01/10 17:33:58 Cleaning up zip file...
[0] > Building: find-python.
Clearing temporary build folder: ./build/find-python/
Preparing ./find-python/ ./build/find-python/function
Building: adsantos/find-python with python template. Please wait..
Sending build context to Docker daemon   7.68kB
Step 1/16 : FROM python:2.7-alpine
 ---> 64905abbb69e
Step 2/16 : RUN apk --no-cache add curl     && echo "Pulling watchdog binary from Github."     && curl -sSL https://github.com/openfaas/faas/releases/download/0.6.9/fwatchdog > /usr/bin/fwatchdog     && chmod +x /usr/bin/fwatchdog     && apk del curl --no-cache
 ---> Using cache
 ---> a31f40d0d1be
Step 3/16 : WORKDIR /root/
 ---> Using cache
 ---> ee8b49ef561e
Step 4/16 : COPY index.py           .
 ---> Using cache
 ---> 851a214e804f
Step 5/16 : COPY requirements.txt   .
 ---> Using cache
 ---> 629b0b406a72
Step 6/16 : RUN pip install -r requirements.txt
 ---> Using cache
 ---> 3db766f5871d
Step 7/16 : RUN mkdir -p function
 ---> Using cache
 ---> 94a007a647c4
Step 8/16 : RUN touch ./function/__init__.py
 ---> Using cache
 ---> e7452223efe5
Step 9/16 : WORKDIR /root/function/
 ---> Using cache
 ---> 768c2a9e21be
Step 10/16 : COPY function/requirements.txt	.
 ---> 6861fedc64a1
Step 11/16 : RUN pip install -r requirements.txt
 ---> Running in 66e6880d997b
Collecting requests (from -r requirements.txt (line 1))
  Downloading requests-2.18.4-py2.py3-none-any.whl (88kB)
Collecting urllib3<1.23,>=1.21.1 (from requests->-r requirements.txt (line 1))
  Downloading urllib3-1.22-py2.py3-none-any.whl (132kB)
Collecting idna<2.7,>=2.5 (from requests->-r requirements.txt (line 1))
  Downloading idna-2.6-py2.py3-none-any.whl (56kB)
Collecting chardet<3.1.0,>=3.0.2 (from requests->-r requirements.txt (line 1))
  Downloading chardet-3.0.4-py2.py3-none-any.whl (133kB)
Collecting certifi>=2017.4.17 (from requests->-r requirements.txt (line 1))
  Downloading certifi-2017.11.5-py2.py3-none-any.whl (330kB)
Installing collected packages: urllib3, idna, chardet, certifi, requests
Successfully installed certifi-2017.11.5 chardet-3.0.4 idna-2.6 requests-2.18.4 urllib3-1.22
Removing intermediate container 66e6880d997b
 ---> 69735c672c93
Step 12/16 : WORKDIR /root/
Removing intermediate container 623605cd782a
 ---> 52b175a4772a
Step 13/16 : COPY function           function
 ---> 1c6508218d5c
Step 14/16 : ENV fprocess="python index.py"
 ---> Running in 9172b97411db
Removing intermediate container 9172b97411db
 ---> 37a9ebe2f24d
Step 15/16 : HEALTHCHECK --interval=1s CMD [ -e /tmp/.lock ] || exit 1
 ---> Running in becff9732748
Removing intermediate container becff9732748
 ---> 31ffcad9833c
Step 16/16 : CMD ["fwatchdog"]
 ---> Running in 20ba4510b557
Removing intermediate container 20ba4510b557
 ---> fd95ba7f9564
Successfully built fd95ba7f9564
Successfully tagged adsantos/find-python:latest
Image: adsantos/find-python built.
[0] < Builder done.

anderson@mac-as:find$ faas push -f ./find-python.yml
[0] > Pushing: find-python.
The push refers to repository [docker.io/adsantos/find-python]
8c26f038403c: Pushed
fe8fd0a167d2: Pushed
0e50bcaa47a5: Pushed
d46972969757: Mounted from adsantos/hello-python
12de77f0d8ff: Mounted from adsantos/hello-python
19ad1c5282b9: Mounted from adsantos/hello-python
4a858ca9581f: Mounted from adsantos/hello-python
d5fde5b67719: Mounted from adsantos/hello-python
837ac7382d51: Mounted from adsantos/hello-python
b1dc8ab0e170: Mounted from adsantos/hello-python
c5130c42f015: Mounted from adsantos/hello-python
7c5ea328fb33: Mounted from adsantos/hello-python
52a5560f4ca0: Mounted from adsantos/hello-python
latest: digest: sha256:d80ec6bd124b43f3c77ce9342129eacc340cc71ddb7fcac231bb9460cedd9ac7 size: 3036
[0] < Pushing done.

anderson@mac-as:find$ faas deploy -f ./find-python.yml
Deploying: find-python.
No existing function to remove
Deployed.
URL: http://virtualbox:31112/function/find-python

202 Accepted

```

# Verify

```bash
anderson@mac-as:find$ docker images | grep find-python
adsantos/find-python           latest              fd95ba7f9564        3 minutes ago       88.1MB

anderson@mac-as:find$ faas list -g http://virtualbox:31112
Function                      	Invocations    	Replicas
find-python                   	0              	1
hello-python                  	8              	1
```


# Run

```bash
anderson@mac-as:find$ curl virtualbox:31112/function/find-python --data-binary '{
"url": "https://blog.alexellis.io/rss/",
"term": "docker"
}'
{"found": true}

anderson@mac-as:find$ curl virtualbox:31112/function/find-python --data-binary '{
"url": "https://www.kubernetes.io/",
"term": "docker"
}'
{"found": false}

anderson@mac-as:find$ curl virtualbox:31112/function/find-python -d '
{
"url": "https://github.com/asantos2000",
"term": "Anderson"
}'
{"found": true}

anderson@mac-as:find$ echo '{"url": "https://github.com/asantos2000", "term": "Anderson"}' | faas invoke find-python -g http://virtualbox:31112
{"found": true}
```

# Referências
1. https://blog.alexellis.io/first-faas-python-function/
2. https://blog.alexellis.io/quickstart-openfaas-cli/