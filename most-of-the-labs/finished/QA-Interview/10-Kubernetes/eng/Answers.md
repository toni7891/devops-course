# Kubernetes Interview Answers

**Q1. How to do maintenance activity on a K8s node?**
Maintenance activities are an inevitable part of administration — you may need to patch or apply security fixes on K8s. Mark the node unschedulable and then drain the PODs present on it.

- `kubectl cordon <hostname>`
- `kubectl drain --ignore-daemonsets <hostname>`

It's important to include `--ignore-daemonsets` for any DaemonSet running on this node. If a StatefulSet is running on this node and no other node is available to maintain its replica count, the StatefulSet POD will be in pending status.

**Q2. What is the role of a pause container?**
The pause container serves as the parent container for all containers in a POD.

- It serves as the basis of Linux namespace sharing in the POD.
- It is PID 1 for each POD, reaping zombie processes.

https://www.ianlewis.org/en/almighty-pause-container

**Q3. Why do we need a service mesh?**
A service mesh ensures that communication among containerized and often ephemeral application infrastructure services is fast, reliable, and secure. It provides critical capabilities including service discovery, load balancing, encryption, observability, traceability, authentication and authorization, and support for the circuit breaker pattern.

**Q4. How to control the resource usage of a POD?**
With requests and limits, the resource usage of a POD can be controlled.

- **request**: the amount of resources being requested for a container. If a container exceeds its request, it may be throttled back down to it.
- **limit**: an upper cap on the resources a container is able to use. If it tries to exceed this limit it may be terminated if Kubernetes decides another container needs the resources. If you're sensitive to pod restarts, the sum of all container resource limits should be equal to or less than the total resource capacity of your cluster.

https://www.noqcks.io/notes/2018/02/03/understanding-kubernetes-resources/

**Q5. What are the units of CPU and memory in a POD definition?**
CPU is in millicores and memory is in bytes. CPU can be easily throttled but memory cannot.

**Q6. Where else can we set a resource limit?**
You may also set a resource limit on a namespace. This is helpful in scenarios where people have a habit of not defining resource limits in the POD definition.

**Q7. How will you update the version of K8s?**
Before updating K8s, it's important to read the release notes to understand the changes introduced in the newer version and whether the version update will also update etcd.

https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade-1-12/

**Q8. What is the difference between Helm and a K8s Operator?**
An Operator is an application-specific controller that extends the Kubernetes API to create, configure, and manage instances of complex stateful applications on behalf of a Kubernetes user. It builds upon basic Kubernetes resource and controller concepts but also includes domain or application-specific knowledge to automate common tasks better managed by computers. Helm, on the other hand, is a package manager like yum or apt-get.

**Q9. Explain the role of CRD (Custom Resource Definition) in K8s?**
A custom resource is an extension of the Kubernetes API that is not necessarily available in a default Kubernetes installation. It represents a customization of a particular Kubernetes installation. Many core Kubernetes functions are now built using custom resources, making Kubernetes more modular.

**Q10. What are the various K8s-related services running on nodes, and what is the role of each?**
A K8s cluster mainly consists of two types of nodes: master and executor.

- Master services:
  - **kube-apiserver**: master API service which acts as the door to the K8s cluster.
  - **kube-scheduler**: schedules PODs according to available resources on executor nodes.
  - **kube-controller-manager**: a control loop that watches the shared state of the cluster through the apiserver and makes changes attempting to move the current state towards the desired state.

- Executor node services (these also run on the master node):
  - **kube-proxy**: the Kubernetes network proxy runs on each node, reflecting services defined in the Kubernetes API and doing simple TCP, UDP, and SCTP stream forwarding or round-robin forwarding across a set of backends.
  - **kubelet**: takes a set of PodSpecs provided through various mechanisms (primarily through the apiserver) and ensures the containers described in those PodSpecs are running and healthy.

**Q11. What is the recommended way of managing access to multiple clusters?**
`kubectl` looks for a config file where multiple clusters' access information can be specified. `kubectl config` commands can be used to manage access to these clusters.

**Q12. What is PDB (Pod Disruption Budget)?**
A PDB specifies the number of replicas an application can tolerate having, relative to how many it is intended to have. For example, a Deployment with `.spec.replicas: 5` is supposed to have 5 pods at any given time. If its PDB allows for there to be 4 at a time, the Eviction API will allow voluntary disruption of one, but not two, pods at a time. This applies to voluntary disruptions.

**Q13. In what situations are DaemonSets normally used?**
DaemonSets are used to start PODs on every node in the cluster. They are generally used to run monitoring or logging agents that are supposed to run on every executor node in the cluster.

**Q14. When are StatefulSets preferred?**
When running applications that require quorum — applications that are not truly stateless — StatefulSets are required.

**Q15. What is an init container and when can it be used?**
Init containers set a stage for you before running the actual POD.

- Wait for some time before starting the app container, with a command like `sleep 60`.
- Clone a git repository into a volume.

**Q16. What are the application deployment strategies?**
In this agile world there is continuous demand to upgrade applications. We have multiple options for deploying a new version of an app:

1. **Recreate**: old style — the existing application version is destroyed and the new version is deployed. Significant downtime.
2. **Rolling update**: gradually bringing down the existing deployment and introducing the new version. You decide how many instances can be upgraded at a single point in time.
3. **Shadow**: traffic going to the existing version is replicated to the new version to see if it's working. Istio provides this pattern.
4. **A/B testing using Istio**: running multiple variants of an application together and determining the best one based on user traffic. More of a management decision.
5. **Blue/Green**: mainly about switching traffic from one version of an app to another.
6. **Canary deployment**: a certain percentage of traffic is shifted from one version to another. If things work well, you keep increasing the traffic shift. It differs from rolling update in that the existing version's count is reduced gradually.

**Q17. How to troubleshoot if a POD is not getting scheduled?**
Many factors can lead to an unstartable POD. The most common is running out of resources. Use commands like `kubectl describe <POD> -n <Namespace>` to see the reason a POD is not started. Also keep an eye on `kubectl get events` to see all events coming from the cluster.

**Q18. How to run a POD on a particular node?**
Various methods are available to achieve this:

- **nodeName**: specify the node name in the POD spec; it will try to run the POD on that specific node.
- **nodeSelector**: assign a specific label to a node with special resources and use the same label in the POD spec so the POD will run only on that node.
- **node affinities**: `requiredDuringSchedulingIgnoredDuringExecution` and `preferredDuringSchedulingIgnoredDuringExecution` are hard and soft requirements for running a POD on specific nodes. This will replace nodeSelector in the future. It depends on node labels.

**Q19. How to ensure PODs are colocated to get performance benefits?**
`podAntiAffinity` and `podAffinity` are the affinity concepts for keeping (or not keeping) PODs on the same node. The key point is that it depends on POD labels.

**Q20. What are taints and tolerations?**
Taints allow a node to repel a set of pods. You can set taints on a node, and only PODs with tolerations matching the taint condition will be able to run on those nodes. This is useful when you've allocated a node for one user and don't want PODs from other users running on that node.

**Q21. How to provide persistent storage for a POD?**
Persistent volumes are used for persistent POD storage. They can be provisioned statically or dynamically.

- **Static**: a cluster administrator creates a number of PVs, carrying the details of the real storage available for use by cluster users.
- **Dynamic**: an administrator creates a PVC (Persistent Volume Claim) specifying an existing storage class, and the volume is created dynamically based on the PVC.

**Q22. How do two containers running in a single POD share a single IP address?**
Kubernetes implements this by creating a special container for each pod whose only purpose is to provide a network interface for the other containers. This is the `pause` container, responsible for namespace sharing in the POD. People generally ignore its existence, but it's actually the heart of the network and other functionalities of the POD — it provides a single virtual interface used by all containers running in a POD.

**Q23. What are the various ways to provide external world connectivity to K8s?**
By default a POD can reach the external world, but for the reverse some work is needed. Options include:

- NodePort (exposes one port on each node to communicate with it)
- Load balancers (L4 layer of TCP/IP)
- Ingress (L7 layer of TCP/IP)

Another method is `kube-proxy`, which can be used to expose a service with only a cluster IP on a local system port:

```
kubectl proxy --port=8080
http://localhost:8080/api/v1/proxy/namespaces/<NAMESPACE>/services/<SERVICE-NAME>:<PORT-NAME>/
```

https://medium.com/google-cloud/kubernetes-nodeport-vs-loadbalancer-vs-ingress-when-should-i-use-what-922f010849e0

**Q24. What is the difference between NodePort and a load balancer?**
NodePort relies on the IP address of your node, and you can only use node ports in the range 30000–32767. A load balancer has its own IP address. All major cloud providers support creating an LB for you if you specify the LB type when creating the service. On bare-metal clusters, MetalLB is a promising option.

**Q25. When do we need Ingress instead of a load balancer?**
For each service you'd otherwise need one LB. You can have a single Ingress for multiple services, allowing both path-based and subdomain-based routing to backend services, and you can do SSL termination at the Ingress.

**Q26. How does POD-to-POD communication work?**
For POD-to-POD communication, it's always recommended to use the K8s service DNS instead of POD IP, because PODs are ephemeral and their IPs can change after redeployment.

If two PODs are running on the same host, the physical interface doesn't come into play:

- A packet leaves POD1's virtual network interface and goes to the docker bridge (`cbr0`).
- The docker bridge forwards the packet to POD2, which is running on the same host.

If two PODs are running on different hosts, the physical interfaces of both host machines come into play. Consider a scenario where a CNI is not used:

```
POD1 = 192.168.2.10/24 (node1, cbr0 192.168.2.1)
POD2 = 192.168.3.10/24 (node2, cbr1 192.168.3.1)
```

- POD1 sends traffic destined for POD2 to its gateway (`cbr0`) because both are in different subnets.
- The gateway doesn't know about the `192.168.3.0/24` network, so it forwards traffic to node1's physical interface.
- node1 forwards the traffic to its own physical router/gateway.
- That physical router/gateway should have a route for `192.168.3.0/24` to route traffic to node2.
- Once traffic reaches node2, it passes that traffic to POD2 through `cbr1`.

With Calico CNI, it's responsible for adding routes for the cbr (docker bridge IP address) on all nodes.

**Q27. How does POD-to-service communication work?**
Because PODs are ephemeral and their IP addresses can change, a service is used as a proxy/load balancer to communicate with PODs reliably. A service is a Kubernetes resource that configures a proxy to forward requests to a set of pods. The set of pods receiving traffic is determined by the selector, which matches labels assigned to pods at creation time. K8s provides an internal cluster DNS that resolves the service name.

A service uses a different internal network than the POD network — netfilter rules injected by `kube-proxy` redirect requests destined for the service IP to the right POD.

**Q28. How does a service know about healthy endpoints?**
The `kubelet` running on a worker node is responsible for detecting unhealthy endpoints. It passes that information to the API server, which eventually passes it to `kube-proxy`, which adjusts the netfilter rules accordingly.

Recommended reading for K8s networking:

https://medium.com/google-cloud/understanding-kubernetes-networking-pods-7117dd28727

https://medium.com/google-cloud/understanding-kubernetes-networking-services-f0cb48e4cc82

https://medium.com/google-cloud/understanding-kubernetes-networking-ingress-1bc341c84078

**Q29. What are the various things that can be done to increase K8s security?**
This is a huge topic — some key practices:

- By default, a POD can communicate with any other POD; set up network policies to limit communication between PODs.
- RBAC (Role Based Access Control) to narrow down permissions.
- Use namespaces to establish security boundaries.
- Set admission control policies to avoid running privileged containers.
- Turn on audit logging.

**Q30. How to monitor a K8s cluster?**
Prometheus is used for K8s monitoring. The Prometheus ecosystem consists of multiple components:

- The main Prometheus server, which scrapes and stores time series data.
- Client libraries for instrumenting application code.
- A push gateway for supporting short-lived jobs.
- Special-purpose exporters for services like HAProxy, StatsD, Graphite, etc.
- An alertmanager to handle alerts.
- Various support tools.

**Q31. How to make Prometheus highly available (HA)?**
You can run multiple Prometheus instances for HA, but Grafana can use only one of them as a datasource. You can put a load balancer in front of multiple Prometheus instances, use sticky sessions, and failover if one instance dies — this makes things complicated. Thanos is another project that solves these challenges.

**Q32. What are other challenges with Prometheus?**
Despite being very good at K8s monitoring, Prometheus still has some issues:

- HA support.
- No downsampling available for collected metrics over time.
- No support for object storage for long-term metric retention.

All of these challenges are again overcome by Thanos.

**Q33. What is the Prometheus Operator?**
The mission of the Prometheus Operator is to make running Prometheus on top of Kubernetes as easy as possible, while preserving configurability and making the configuration Kubernetes-native.

**Q34. How to get centralized logs from a POD?**
This architecture depends on the application and many other factors. Common logging patterns include:

- Node-level logging agent
- Streaming sidecar container
- Sidecar container with a logging agent
- Exporting logs directly from the application

A common setup runs `filebeat` and `journalbeat` as DaemonSets. Logs collected by these are dumped to a Kafka topic, which is eventually dumped to the ELK stack. The same can be achieved using the EFK stack and Fluent Bit.
