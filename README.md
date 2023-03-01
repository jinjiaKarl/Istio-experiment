# Test Istio performance in different scenarios

My seminar paper experiment for CS-E4000 - Seminar in Computer Science

# Prerequisites
* [minikube](https://minikube.sigs.k8s.io/docs/)
* [istio](https://istio.io/)
* [fortio](https://github.com/fortio/fortio)

# Run
I test it on my own laptop, MacOs 13.1 baed on ARM chip.

## Mutual TLS
```
cd benchmark
eval $(minikube -p minikube docker-env)
docker compose build
kubectl apply -f mtls.yaml
kubectl apply -f fortio-server.yaml
kubectl apply -f fortio-client.yaml
kubectl apply -f fortio-gateway.yaml

kubectl exec `kubectl get pod -l app=fortio-client -o  jsonpath='{.items[0].metadata.name}'` -it -- fortio server

# open browser and go to http://localhost/client/fortio/ and the target url is http://fortio-server:8080/echo
```

If you want show the result that I have done, you can run the following command:
```
cd benchmark
fortio report 

# open browser and go to http://localhost:8080/
```

TODO
* turn off mTLS
* calculate the netfilter overhead and bpf overhead using perf and eBPF
* test other server mesh mode
    * grpc proxyless (Istio)
    * Istio ambient
    * Cilium Service Mesh