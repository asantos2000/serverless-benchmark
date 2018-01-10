# Installing kubernetes cluster
References: [How to quickly install Kubernetes on Ubuntu](https://www.techrepublic.com/article/how-to-quickly-install-kubernetes-on-ubuntu/)
What we're going to install below must be installed on all machines that will be joining the cluster. 

## Infrastructure

```
master <- node01
       <- node02
       <- node03
```

### Machines
Virtual machines at Vivo Cloud, with 2vCPU, 2GB of RAM memory, 40GB of SSD storage, one network interface, and full access of internet.

#### Master
```
Hostname: ariel
inet addr:10.100.18.10  Bcast:10.100.18.255  Mask:255.255.255.0
inet6 addr: fe80::f816:8eff:fe81:24c6/64 Scope:Link

$ ssh linux@10.100.18.10 -i id_rsa
```

#### Node01
```
Hostname: mimas
inet addr:10.100.18.11  Bcast:10.100.18.255  Mask:255.255.255.0
inet6 addr: fe80::f816:8eff:fe92:17f5/64 Scope:Link

$ ssh linux@10.100.18.11 -i id_rsa
```

#### Node02
```
Hostname: thor
inet addr:10.100.18.12  Bcast:10.100.18.255  Mask:255.255.255.0
inet6 addr: fe80::f816:8eff:fe5e:636b/64 Scope:Link

$ ssh linux@10.100.18.12 -i id_rsa
```

#### Node03
```
Hostname: lupus
inet addr:10.100.18.13  Bcast:10.100.18.255  Mask:255.255.255.0
inet6 addr: fe80::f816:8eff:fe54:7e9/64 Scope:Link

$ ssh linux@10.100.18.13 -i id_rsa
```

#### Internet addresses
```
200.196.230.174 -> ariel (master)
200.196.251.26  -> mimas (node01)
200.196.251.119 -> thor  (node02)
200.196.251.243 -> lupus (node03)
```
Ports opened on firewall

```
TCP 80
TCP 443
TCP 6443
TCP 1883
TCP 2376
TCP 2377
TCP 2379
TCP 2380
UDP 4789
TCP 5000
TCP 5672
TCP 7946
UDP 7946
UDP 8472
TCP 8883
TCP 9765
TCP 10250
TCP 10251
TCP 10252
TCP 10255
TCP 30080
TCP 30088
```

#### Testando a conectividade
Execute o script abaixo para cada máquina do cluster:

```bash
$ vi test-conn.sh

nc -z -v -w5 $1 80
nc -z -v -w5 $1 443
nc -z -v -w5 $1 6443
nc -z -v -w5 $1 1883
nc -z -v -w5 $1 2376
nc -z -v -w5 $1 2377
nc -z -v -w5 $1 2379
nc -z -v -w5 $1 2380
nc -z -v -w5 $1 4789
nc -z -v -w5 $1 5000
nc -z -v -w5 $1 5672
nc -z -v -w5 $1 7946
nc -z -v -w5 $1 7946
nc -z -v -w5 $1 8472
nc -z -v -w5 $1 8883
nc -z -v -w5 $1 9765
nc -z -v -w5 $1 10250
nc -z -v -w5 $1 10251
nc -z -v -w5 $1 10252
nc -z -v -w5 $1 10255
nc -z -v -w5 $1 30080
nc -z -v -w5 $1 30088
```

## Installing docker

### Installing dependencies

```bash
sudo apt-get update

sudo apt-get install -y apt-transport-https
```

### Next dependency is Docker

```bash
$ sudo apt install docker.io
```

### Start and enable the Docker service

```bash
$ sudo systemctl start docker

$ sudo systemctl enable docker
```

Test your docker installation

```bash
$ docker --version
Docker version 1.13.1, build 092cba3

$ docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
ca4f61b1923c: Pull complete
Digest: sha256:be0cd392e45be79ffeffa6b05338b98ebb16c87b255f48e297ec7f98e123905c
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://cloud.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/engine/userguide/
 
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                      PORTS               NAMES
1e8f8ed30b97        hello-world         "/hello"            39 seconds ago      Exited (0) 38 seconds ago                       quizzical_raman

$ docker container prune # clean things up
WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
Deleted Containers:
1e8f8ed30b97900d8ee72a1c5842b54a614e560e8e69fe33f42b3b7c655a9630

$ docker image rm hello-world # clean things up
Untagged: hello-world:latest
Untagged: hello-world@sha256:be0cd392e45be79ffeffa6b05338b98ebb16c87b255f48e297ec7f98e123905c
Deleted: sha256:f2a91732366c0332ccd7afd2a5c4ff2b9af81f549370f7a19acd460f87686bc7
Deleted: sha256:f999ae22f308fea973e5a25b57699b5daf6b0f1150ac2a5c2ea9d7fecee50fdf
```

### Add user to the docker group

```bash
$ sudo gpasswd -a $USER docker
Adding user linux to group docker
```

> Exit and log again.

## Installing Kubernetes

### Download and add the key for the Kubernetes install.

```bash
sudo curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add
```

### Add a repository
```bash
$ sudo vi /etc/apt/sources.list.d/kubernetes.list
```

Enter the following content:

```
deb http://apt.kubernetes.io/ kubernetes-xenial main 
```

Save and close that file.

### Install Kubernetes

```bash
$ sudo apt-get update

$ sudo apt-get install -y kubelet kubeadm kubectl kubernetes-cni
```

### Disabling linux swap

```bash
$ sudo swapoff -a 
```

Comment swap line at /etc/fstab.

### Initialize the cluster

#### Init master
> **Attention**: Execute the following commands only in the Master machine.

```bash
$ sudo kubeadm init --pod-network-cidr 10.244.0.0/16

Your Kubernetes master has initialized successfully!

To start using your cluster, you need to run (as a regular user):

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  http://kubernetes.io/docs/admin/addons/

You can now join any number of machines by running the following on each node
as root:

  kubeadm join --token 0f4ce3.5ddf0f259f4e02f1 10.100.18.10:6443
```
Ref: [Stackoverflow: kube-dns stays in ContainerCreating status](https://stackoverflow.com/questions/41466935/kube-dns-stays-in-containercreating-status/42310610#42310610)

##### Config file
```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUN5RENDQWJDZ0F3SUJBZ0lCQURBTkJna3Foa2lHOXcwQkFRc0ZBREFWTVJNd0VRWURWUVFERXdwcmRXSmwKY201bGRHVnpNQjRYRFRFNE1ERXdOVEl3TWpneE5sb1hEVEk0TURFd016SXdNamd4Tmxvd0ZURVRNQkVHQTFVRQpBeE1LYTNWaVpYSnVaWFJsY3pDQ0FTSXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBT0hHCm5pYWxjMFVsbm05ajVXVlZDZjI0TGNabHIyalp5dzVxdzdPS2psQ09leWJHU0UzUVJjNXEvSkRKOUdueTc4WE0KS0FJMVVBSVhQOG15U3JoTlp3Tmx0M0xSRkg4Ni8yUVlVVVJzQ0pwSmJWWmg2Tll5dGJVenlRWVlRVlhrMFhzVwpINWhSQW4yaWY0TktHWnRrY0V0K0ZValV3SWN2RFFmeXBnRStuUzhidXg0K0ROM0hQSE9hc2hkMzNLUWtUdG1yCjY1eXZ3M3doNHlhdS9iSWtUeU1IdTQ1NzFHZUpROGpnOHpwMHZLcmloYVJMN2JkUndKN2pUMkUwanQwQ1BMbjUKZ3RWVXQzcmNpSzJxb2tQcXhvTmhLanE4TDUxUG5ESkhaZyt2WkRHeHM2UUoyNzJrUDFseWxQSDVKOUIzVDZ0aAp2NmdTWS9UM084UTlQYWZhNGpNQ0F3RUFBYU1qTUNFd0RnWURWUjBQQVFIL0JBUURBZ0trTUE4R0ExVWRFd0VCCi93UUZNQU1CQWY4d0RRWUpLb1pJaHZjTkFRRUxCUUFEZ2dFQkFINFBEMll2Rm1nUndZMGlGa2xvN2R1U3FqUEQKV0NWbmtCMFFVUnFoODFCYlM5a0QxZkxNQkk3b29zTXZubU9kd0l1MzRCZThFendWZzlES2NSSy9GQU80OXNHQgp2cUNyWUpkU3ZtZXhWNUdiemIweUNlNEJ4RzVMNGVoRXMzdDhxWlkrblpObkIzVmZ1TDEwa204ajdLQ2ZwdnMrClpnODA1ZUtmaXlCV2JVdENOalJ6Uk9PcUFrd0hGd21EUENRbFpoVlByUVFnMEU3bWszMXUrZUQ4bFgyb0ExYnkKNmVwdWdUQ0FaamZqeDRTMCt3bkdJZnMxWnJHVzRVajAxejNhVFBEQjNiWXNKMzVwaHpMYmMyelBQTzJrRzJPYwplazVGMlp6VEtFMEhpRkNzbEVmU1pEYTY0dHNWaU9zS0VHbVdyWVJSWnk1ZFNTV2FTb1Y0NmRkWkhZQT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=
    server: https://10.100.18.10:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: kubernetes-admin
  name: kubernetes-admin@kubernetes
current-context: kubernetes-admin@kubernetes
kind: Config
preferences: {}
users:
- name: kubernetes-admin
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUM4akNDQWRxZ0F3SUJBZ0lJVWtRWVp5MVFEam93RFFZSktvWklodmNOQVFFTEJRQXdGVEVUTUJFR0ExVUUKQXhNS2EzVmlaWEp1WlhSbGN6QWVGdzB4T0RBeE1EVXlNREk0TVRaYUZ3MHhPVEF4TURVeU1ESTRNVGxhTURReApGekFWQmdOVkJBb1REbk41YzNSbGJUcHRZWE4wWlhKek1Sa3dGd1lEVlFRREV4QnJkV0psY201bGRHVnpMV0ZrCmJXbHVNSUlCSWpBTkJna3Foa2lHOXcwQkFRRUZBQU9DQVE4QU1JSUJDZ0tDQVFFQXYrSzU0QWpYdUZsU3c5QmUKV2RmalBvVCt1TklUWFArR3k5ZWFoNjVFTForWFFzaDZiUW8xKzFhdVpxcnhWYXVudWJYbTVJTFY2QjNJNTRjbQpwamd3dnBOc3l2ek1tUDFzUTRxRHBXbENXbElqQ3QrYkRwWXlFVHZySDZUMUNwVzg4N0kxZW1CRTY2cEhNbWlGCnM0SGNmK0syOEtHM2xZUmt6bHgzMG0yTkZpVzZqUlhnQ2VTZUJKVWNZbHhCT3ZFTVR6b0VJZE9PMjRnQmVTRTQKUHhvQ2xnaDUxS0lNSlFvV0MxZGMvQVlVZ3hQaW9zeExwbXEzQTBteFpyZDBDUHo4NHZQTERvTUp4azhZVkUvdApnTllEb1F4YUlvaDRpNU1OOXRmc2pjTzU3UzlWeCtuR1J1U3FYN2tRLzNabjc1WGJXdGdSTDRZWU9MMVA1dmkxCkpaNlo2UUlEQVFBQm95Y3dKVEFPQmdOVkhROEJBZjhFQkFNQ0JhQXdFd1lEVlIwbEJBd3dDZ1lJS3dZQkJRVUgKQXdJd0RRWUpLb1pJaHZjTkFRRUxCUUFEZ2dFQkFER1I1b0hUeTZ3S21LOHBKa2Z4QmVOY3YzNTMwMENoS2JlRQovK1lReGpQdlU1NE4vbytLOGtoV0lHMDkrcFcxK1UvblNxWXo3ZUR3dXkzakt1ZkZjMER4enJUUmI1M25nRllnCnQzOWpqUzNyUGFDcWE2b2xUdzhid1MyS2FLQVNlZXp4R2RKT2pGY3I0SUZEcGt2TUlzNW0wMjhQcWFHVEUwMWsKZmFUR3J6NHB6ckpVTDgvY29mUThlcW9TcHFOMXVJdTBZRm5HSW9jcXVoQnJyK2QzRGpBbnBnQ3F2MWt1YW1pcQpzUnVQVExhNlR3MDZoTklGbzBzV29jYVI2b0hBY3M2Y2xyRitKSldXcFM2aTJaVUcrVWlIYjFDMU9DSHM1TlVBCkZBcjlXR0lvQXpha1JoTjJ1eE9jRlpOMHhFUzFBVUIrMVFteXdNNDBJMXh6eE1ENnFobz0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=
    client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcFFJQkFBS0NBUUVBditLNTRBalh1RmxTdzlCZVdkZmpQb1QrdU5JVFhQK0d5OWVhaDY1RUxaK1hRc2g2CmJRbzErMWF1WnFyeFZhdW51YlhtNUlMVjZCM0k1NGNtcGpnd3ZwTnN5dnpNbVAxc1E0cURwV2xDV2xJakN0K2IKRHBZeUVUdnJINlQxQ3BXODg3STFlbUJFNjZwSE1taUZzNEhjZitLMjhLRzNsWVJremx4MzBtMk5GaVc2alJYZwpDZVNlQkpVY1lseEJPdkVNVHpvRUlkT08yNGdCZVNFNFB4b0NsZ2g1MUtJTUpRb1dDMWRjL0FZVWd4UGlvc3hMCnBtcTNBMG14WnJkMENQejg0dlBMRG9NSnhrOFlWRS90Z05ZRG9ReGFJb2g0aTVNTjl0ZnNqY081N1M5VngrbkcKUnVTcVg3a1EvM1puNzVYYld0Z1JMNFlZT0wxUDV2aTFKWjZaNlFJREFRQUJBb0lCQVFDUmZqd3Azd3FTUVVnOApLUlloVVV5QTd4Nmt6TVRaMHZaR1FXaHVVSGhwajRTRm9yVVJVSmkxeG5mZWFPY3Nha2QyekxJUnVoS3ZPVVpJCkozWHF1dGhhNkRXcGhCMHVNNW1QYk10ODlGN1hWVWcweW04cmxEN0tTb0J4TWdhS3pCYkZRTzdEcDVNYWpiWUcKUnJKNTlaRlhkblAzNk9ibWU4aGpvRUZLVUw2VmR4MUJYNExCaDlpdjN2K2hoRDZJeElPZzVTckhNTHZTSmVvVApCcVg0dnhBa3o4WDBwNlhhc0w5dmNHd3JMY1AycTlrNkZQZnBkelVmeXM0bWlHT2RNY05FT2N1Yk9LeGZsUm0zCkdObG9lWWFsb3pNUE1hdW5vS3BtRjNycWVKTU9PTkY5TkYzTUt0cFhkWktzQzJGdVIyV2VOb3QxVk5lV3FBREIKV25qWVlFY3hBb0dCQU93VEM3TDhIL1pBcEhJanYyOWoxZlVvMDBlV3VFbFJrdG9UYnVCY3RjdVlMMGlpTENETQpBMGx0OHp5U1lRSHlaRk5XWTN3bndjaDkvbEV0ODFUa0pDeENlcEpIRVkwbG44anc5VmZIV2JCMkRGVTh0aWxDCldtb25tc3N1eEsxRzJXbEF0S3haZjVjYk50Z2hhcThLUk04QXphbG5ZVUcwTDJkRDVNbk5XUFJmQW9HQkFOQVUKNEZmZW9IQUJKUEtIOUF4dzhRZVZvaXNvMnV2WHVDSzI4akwxdHljMUUwOWlVb0R4TEw4TjhtdG5ROXA0aVJFSApvZndJMERjL2FxcjB5cFRINGNiT3haZUxqdC9aU05NNjgzY1RRVVVaQlhTdGxOaGJULzlwN09jQWpxd0NhSGkvCmViVDRuMHdzREhhT1k2K0lHMjMxWC9vM0laNVlpajVsWjd5dEVGYTNBb0dCQUlMV1kydUZkS2xrVmorME5Fc20KQjlUaUZZYmRyN0ZpOW9MS3RtNitzenJ0VTNkcitnMExSTjhUZ3ZXVkl4S1RKcXRSZTcyNXd4cTlTWS93YWFZbwo4eXRjaE5aQmNTYkxMVzJPcmt0Qi95RmZxNklxRGNOOE5PUVVveVBzL2JBVFRqZVpWd2tXYVRKME1NZEViZjRwCk1NMlJZbXA3RTFuNDVUVFVXaDdHSW9EOUFvR0JBTGFuSEtjRlRXQUVJU0trSko0bkpleTZkTGZlRFEycE5vR0MKaGVnbHVMZzU1dEZ3Uld2YVNLVU00UmRXZGtGNFBSa3QwZ3NpMFdNdHo3eHhWTUoxRXNNcERsbVFyOEhmUWdYcApZWDNNOFNadWFGT2JhMlRnQXNENWduTGtFbGo3WkNsYUtzT28ybXhLM2tYVGg3MjFoQjVwbmU1T0pyeVFqQWxwCmlqNGN6SkxSQW9HQUNrMWM1d2dsdDNZbXlyREhGc3JvQ3FneUJZcXV0bTBFblc0ZTlRWkR5TE92YkpqUnhkcDAKUjZvNmovWDNtcVdHUjlyOGZJZmFYRFJKUHZsTHhCUHdYU0ttWVE3YkZUQTRZeFNsVlVFMG01bm1LelJhZkd3MwpkaUszaUtLREhTYmZlbjk0WE02ZlZLQ0Y4d2h1ckkraHlOOFhPY3RWVk1FSDVKRzY5UHA5MHRNPQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQo=
```

##### Before join nodes
> Run on Master

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

##### Deploying a pod network
> Run following commands only on the Master machine.

```bash
$ sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

##### Testing
```bash
linux@thor:~$ kubectl get pods --all-namespaces
NAMESPACE     NAME                                    READY     STATUS    RESTARTS   AGE
kube-system   etcd-ariel                              1/1       Running   0          1h
kube-system   kube-apiserver-ariel                    1/1       Running   0          6m
kube-system   kube-controller-manager-ariel           1/1       Running   0          6m
kube-system   kube-dns-6f4fd4bdf-ndgjw                3/3       Running   0          1h
kube-system   kube-flannel-ds-2sdm7                   1/1       Running   18         1h
kube-system   kube-flannel-ds-fsvnd                   1/1       Running   19         1h
kube-system   kube-flannel-ds-j8brn                   1/1       Running   18         1h
kube-system   kube-flannel-ds-xs2qm                   1/1       Running   18         1h
kube-system   kube-proxy-7llr5                        1/1       Running   0          1h
kube-system   kube-proxy-qcs85                        1/1       Running   0          1h
kube-system   kube-proxy-qsccv                        1/1       Running   0          1h
kube-system   kube-proxy-t6gx2                        1/1       Running   0          1h
kube-system   kube-scheduler-ariel                    1/1       Running   0          1h
```

#### Installing dashboard
References: [Dashboard](https://github.com/kubernetes/dashboard), [Access Control](https://github.com/kubernetes/dashboard/wiki/Access-control)

Starts running: 

```bash
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml
```

Afert pod is running

```bash
linux@thor:~$ kubectl get pods --all-namespaces
NAMESPACE     NAME                                    READY     STATUS    RESTARTS   AGE
kube-system   etcd-ariel                              1/1       Running   0          1h
kube-system   kube-apiserver-ariel                    1/1       Running   0          6m
kube-system   kube-controller-manager-ariel           1/1       Running   0          6m
kube-system   kube-dns-6f4fd4bdf-ndgjw                3/3       Running   0          1h
kube-system   kube-flannel-ds-2sdm7                   1/1       Running   18         1h
kube-system   kube-flannel-ds-fsvnd                   1/1       Running   19         1h
kube-system   kube-flannel-ds-j8brn                   1/1       Running   18         1h
kube-system   kube-flannel-ds-xs2qm                   1/1       Running   18         1h
kube-system   kube-proxy-7llr5                        1/1       Running   0          1h
kube-system   kube-proxy-qcs85                        1/1       Running   0          1h
kube-system   kube-proxy-qsccv                        1/1       Running   0          1h
kube-system   kube-proxy-t6gx2                        1/1       Running   0          1h
kube-system   kube-scheduler-ariel                    1/1       Running   0          1h
kube-system   kubernetes-dashboard-6ddcb6df4c-pjmc4   1/1       Running   0          23s

```

Configure access control using [admin privileges](https://github.com/kubernetes/dashboard/wiki/Access-control#admin-privileges)

Create file dashboard-admin.yaml

```yaml
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: kubernetes-dashboard
  labels:
    k8s-app: kubernetes-dashboard
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: kubernetes-dashboard
  namespace: kube-system
```

And run the command

```bash
$ kubectl create -f dashboard-admin.yaml
```

On your computer run

```bash
mac-as:~$ kubectl proxy
Starting to serve on 127.0.0.1:8001
```

Open on your browser [open dashboard](http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/)

On Login View (Authentication method screen) choose SKIP.

#### Configuring your computer to admin the cluster through command line.

Copy the /etc/kubernetes/admin.conf from the master and save it in your computer as kubeconfig.yml

Open the file ~/.kube/config in your computer, if it not exists just create it with the content of kubeconfig.yaml.

If the file exists (i.e. you're accessing Google Containers) you'll need to merge it with the content of the session in kubeconfig.yaml.

After that you're able to execute the same commands are in the master.

```bash
mac-as:kubernetes$ kubectl get pods --all-namespaces
NAMESPACE     NAME                                    READY     STATUS    RESTARTS   AGE
kube-system   etcd-ariel                              1/1       Running   0          1h
kube-system   kube-apiserver-ariel                    1/1       Running   0          10m
kube-system   kube-controller-manager-ariel           1/1       Running   0          10m
kube-system   kube-dns-6f4fd4bdf-ndgjw                3/3       Running   0          1h
kube-system   kube-flannel-ds-2sdm7                   1/1       Running   18         1h
kube-system   kube-flannel-ds-fsvnd                   1/1       Running   19         1h
kube-system   kube-flannel-ds-j8brn                   1/1       Running   18         1h
kube-system   kube-flannel-ds-xs2qm                   1/1       Running   18         1h
kube-system   kube-proxy-7llr5                        1/1       Running   0          1h
kube-system   kube-proxy-qcs85                        1/1       Running   0          1h
kube-system   kube-proxy-qsccv                        1/1       Running   0          1h
kube-system   kube-proxy-t6gx2                        1/1       Running   0          1h
kube-system   kube-scheduler-ariel                    1/1       Running   0          1h
kube-system   kubernetes-dashboard-6ddcb6df4c-pjmc4   1/1       Running   0          4m
```

#### Join nodes

```bash
$ sudo   kubeadm join --token 163d91.e54df2dea1751e68 10.100.18.10:6443 --discovery-token-ca-cert-hash sha256:ba5b0fccf37381328df209d12e3bb67a5f99c8655485780dd02392b5fb74f6bf

[kubeadm] WARNING: kubeadm is in beta, please do not use it for production clusters.
[preflight] Running pre-flight checks
[discovery] Trying to connect to API Server "10.100.18.10:6443"
[discovery] Created cluster-info discovery client, requesting info from "https://10.100.18.10:6443"
[discovery] Requesting info from "https://10.100.18.10:6443" again to validate TLS against the pinned public key
[discovery] Cluster info signature and contents are valid and TLS certificate validates against pinned roots, will use API Server "10.100.18.10:6443"
[discovery] Successfully established connection with API Server "10.100.18.10:6443"
[bootstrap] Detected server version: v1.8.4
[bootstrap] The server supports the Certificates API (certificates.k8s.io/v1beta1)

Node join complete:
* Certificate signing request sent to master and response
  received.
* Kubelet informed of new secure connection details.

Run 'kubectl get nodes' on the master to see this machine join.
```

### Install Helm

Follow instructions for [installation on specific OS](https://github.com/kubernetes/helm#install).

If does not work, with error above:

> ```anderson@mac-as:fn-helm(master)*$ helm status vivo-poc
Error: getting deployed release "vivo-poc": User "system:serviceaccount:kube-system:default" cannot list configmaps in the namespace "kube-system". (get configmaps)
```

> Ref: [https://github.com/kubernetes/helm/issues/3130](https://github.com/kubernetes/helm/issues/3130) (noprom commented on Nov 14, 2017)

Try

```bash
$ vi rbac-config.yaml
```
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: tiller
  namespace: kube-system
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: tiller-clusterrolebinding
subjects:
- kind: ServiceAccount
  name: tiller
  namespace: kube-system
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: ""
```

```bash
$ kubectl apply -f rbac-config.yaml
```

```bash
$ helm init --service-account tiller --upgrade
```

### Update permission for fnProject

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