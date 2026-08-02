# SAA-C03 Service Study Guide
### Compiled reference — 36 services/topics, simple language, exam-trigger tables

---

## STORAGE & MIGRATION

### 1. AWS Snowball Edge

**What it is:** A physical box AWS mails to you. You load your data onto it, then mail it back. Used when you have a LOT of data and sending it over the internet would take too long.

| Thing | Explanation |
|---|---|
| Why use it | If you have huge amounts of data (TB/PB), sending over internet could take weeks/months. Shipping is faster |
| Rule of thumb | If internet transfer would take more than 1 week, use Snowball instead |
| Two versions | **Storage** = just for moving data. **Compute** = can also run programs (EC2, Lambda) on the device |
| Encryption | Always encrypted automatically (256-bit, KMS-managed) |
| Bigger version | **Snowmobile** = a truck for 10PB+ migrations |
| Smaller version | **Snowcone** = tiny, 8TB, mailable |

**Snow Family Comparison**

| Device | Capacity | Use Case |
|---|---|---|
| Snowcone | 8TB | Small jobs, tight spaces, mailable |
| Snowball Edge (Storage) | 80TB | Large data migration |
| Snowball Edge (Compute) | ~42TB + compute | Remote location needing local processing |
| Snowmobile | Up to 100PB | Moving an entire data center |

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| Huge data, slow/no internet | Snowball Edge (or Snowmobile if massive) |
| Remote location needs local compute/Lambda, no internet | Snowball Edge Compute |
| Ship a physical device to move data | Snowball Edge |
| Moving an entire data center | Snowmobile |
| Small device, low power, easy to mail | Snowcone |
| Internet IS available, just want automated transfer | NOT Snowball → use DataSync |

---

### 2. AWS Storage Gateway

**What it is:** Connects on-site servers to AWS storage in the cloud, making cloud storage act like normal local storage so apps don't need to change.

| Type | What it does | Use case |
|---|---|---|
| **File Gateway** | Stores files in S3, accessed like a normal shared folder (NFS/SMB) | Company file shares, backups |
| **Volume Gateway** | Acts like a hard drive (block storage), backed by S3, EBS snapshots | On-site servers needing disk + cloud backup |
| **Tape Gateway** | Acts like a physical tape backup system, stores in S3/Glacier | Replace physical tape backups |

**Volume Gateway Modes**

| Mode | How it works |
|---|---|
| Cached | Most data in AWS, only frequent data kept locally |
| Stored | Full copy locally, also backed up to AWS |

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| Local file share that also stores in S3 | File Gateway |
| Old tape backup software, want to move to cloud | Tape Gateway |
| On-site server needs disk storage, backed up to cloud | Volume Gateway |
| Replace physical tapes | Tape Gateway |

---

## CONTENT DELIVERY & EDGE NETWORKING

### 3. Amazon CloudFront

**What it is:** A CDN — stores copies of your content at edge locations worldwide so users load it from somewhere nearby, faster.

| Thing | Explanation |
|---|---|
| Origin | Original content source — S3, EC2, Load Balancer |
| Caching | Keeps a copy of files for a set time, avoiding repeated origin requests |
| Security | HTTPS, works with Shield (DDoS) and WAF (bad traffic) |
| Access control | Signed URLs/cookies restrict who can view content |
| Geo restriction | Block/allow access by country |

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| Users worldwide need fast access to content | CloudFront |
| Reduce load on origin server | CloudFront |
| Stream video/audio to many users | CloudFront |
| Only paying/logged-in users access certain files | Signed URLs/cookies |
| Block specific countries | Geo Restriction |
| Private S3 content only via CDN | CloudFront + Origin Access Control |

**Don't confuse with:** Global Accelerator (routes non-cacheable traffic, no caching) or Route 53 (DNS only).

---

### 4. Lambda@Edge

**What it is:** Runs Lambda functions at CloudFront edge locations, close to users — only works with CloudFront.

| Trigger Point | When it Runs |
|---|---|
| Viewer Request | When request first arrives (before cache check) |
| Origin Request | Right before sending to origin (if not cached) |
| Origin Response | Right after getting response from origin |
| Viewer Response | Right before sending response to user |

**Lambda@Edge vs CloudFront Functions**

| Feature | CloudFront Functions | Lambda@Edge |
|---|---|---|
| Language | JavaScript only | Node.js, Python |
| Trigger points | 2 (Viewer Request/Response) | 4 (all points) |
| Complexity | Simple, light logic | Can be complex |
| Calls other AWS services? | No | Yes |
| Speed/Cost | Faster, cheaper | Slightly slower, more powerful |

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| Customize content by device/location at edge | Lambda@Edge |
| Simple, lightweight, very cheap, low latency | CloudFront Functions |
| Complex logic, calls other AWS services | Lambda@Edge |

---

### 5. AWS Global Accelerator

**What it is:** Gives your app 2 fixed IPs and routes traffic through AWS's private network — no caching, just smart routing.

| Thing | Explanation |
|---|---|
| Fixed IPs | 2 static IPs that never change |
| Works with | EC2, ALB/NLB, Elastic IPs |
| Health checks | Fast failover (seconds) to healthy endpoints |
| Multi-region | Routes to closest healthy region |

**CloudFront vs Global Accelerator**

| Feature | CloudFront | Global Accelerator |
|---|---|---|
| Purpose | Caching/delivering content | Speeding up routing, no caching |
| Best for | Static/cacheable content | TCP/UDP, gaming, VoIP, APIs |
| IPs | Domain-based | 2 fixed/static IPs |
| Protocol | HTTP/HTTPS only | Any TCP/UDP |

**Simple rule:** Website needing speed → CloudFront. App needing fixed IPs/fast failover/non-cacheable traffic → Global Accelerator.

---

## COMPUTE

### 6. Amazon EC2 — Hibernation, Spot, Placement Groups

**Hibernation**

| Thing | Explanation |
|---|---|
| Cost while hibernated | Pay only for EBS volume + Elastic IP, not the instance |
| What's saved | RAM contents saved to EBS root volume |
| On restart | RAM reloaded, EBS root volume restored — feels like resuming, not rebooting |

**Spot Instances**

| Thing | Explanation |
|---|---|
| Price | Up to 90% cheaper than On-Demand |
| Risk | AWS can terminate with 2-minute warning |
| Good for | Batch jobs, data analysis, background processing |
| Bad for | Anything needing to run uninterrupted (databases, live customer traffic) |

**Placement Groups** (free to create)

| Type | How it places instances | Best for |
|---|---|---|
| Cluster | Packs close together, one AZ | HPC, low-latency node-to-node |
| Partition | Groups on separate hardware per partition | Hadoop, Cassandra, Kafka |
| Spread | Max separation across hardware | Small number of critical instances |

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| Resume instance quickly with state intact | Hibernation |
| Interruption-tolerant, cost savings | Spot Instances |
| Low latency, tightly-coupled, HPC | Cluster placement group |
| Large distributed workload, failure isolation | Partition placement group |
| Reduce correlated failure risk for small critical group | Spread placement group |

---

### 7. AWS Elastic Beanstalk

**What it is:** Upload your code, AWS automatically handles deployment, capacity, load balancing, scaling, and health monitoring.

| Thing | Explanation |
|---|---|
| Best for | Simple web applications |
| Not ideal for | Microservices |
| Scaling types | Time-based (scheduled) and Dynamic |

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| Quickly deploy simple web app, no infra management | Elastic Beanstalk |
| Known schedule for traffic changes | Time-based scaling |
| Need microservices/complex architecture | NOT Beanstalk → ECS/EKS |

**Don't confuse with:** CloudFormation (defines any infra via code, more flexible/complex), ECS/EKS (containers/microservices), CodeDeploy (just deployment, not full environment).

---

### 8. Amazon ECS (Elastic Container Service)

| Thing | Explanation |
|---|---|
| Service Auto Scaling | Scale tasks based on metrics like CPU utilization |
| Who manages scaling | AWS Application Auto Scaling (also used for DynamoDB, Aurora) |
| Fargate scaling | Use Application Auto Scaling + target tracking policy |
| Fargate + AZs | Tasks automatically spread across AZs by default — built-in HA |

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| Auto scale ECS tasks based on CPU | ECS Service Auto Scaling (target tracking) |
| Ensure HA for Fargate without manual config | Default — Fargate spreads across AZs |
| Scale Fargate tasks to maintain a utilization target | Application Auto Scaling + target tracking |

**Note:** Application Auto Scaling = general tool (ECS, DynamoDB, Aurora). EC2 Auto Scaling = only for EC2 instances themselves (relevant if ECS uses EC2 launch type).

---

### 9. AWS Lambda

| Thing | Explanation |
|---|---|
| Max runtime | 15 minutes per execution |
| Trigger model | Event-driven (S3 upload, API call, SQS message, schedule, etc.) |
| Pricing | Pay only for actual execution time |
| Operational overhead | Lowest of all compute options |

**Overhead Comparison**

| Service | Operational Overhead |
|---|---|
| Lambda | Lowest — no servers, no patching |
| ECS | Medium-High (EC2 launch type) |
| EC2 | High — manage everything yourself |
| EKS | Highest — full Kubernetes cluster |

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| Minimal operational overhead, run code | Lambda |
| Event-driven, short task (<15 min) | Lambda |
| Task runs longer than 15 min or continuously | NOT Lambda → Fargate/ECS/EC2 |
| Containers, longer-running, still serverless | Fargate |

---

## LOAD BALANCING

### 10. Elastic Load Balancers (NLB, ALB) + Session Management

**Network Load Balancer (NLB)**

| Thing | Explanation |
|---|---|
| Layer | 4 (TCP/UDP) |
| Speed | Ultra-low latency |
| Capacity | Tens of millions of requests/sec |
| Best for | Gaming, IoT, real-time, raw TCP/UDP |

**Application Load Balancer (ALB)**

| Thing | Explanation |
|---|---|
| Layer | 7 (HTTP/HTTPS) |
| HTTP→HTTPS redirect | Yes, via listener rule |
| Path-based routing | Routes by URL path to different target groups |
| Best for | Web apps, microservices with multiple paths |

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| Extreme performance, millions of req/sec, TCP/UDP | NLB |
| Route based on URL path/hostname | ALB |
| Redirect HTTP to HTTPS | ALB |

**Session Management**

| Option | How it works | Drawback |
|---|---|---|
| Sticky Sessions | LB always sends same user to same server | Lost on node failure; uneven ASG distribution |
| Distributed Session (ElastiCache Redis/Memcached) | Shared storage, any server can read it | Extra cost/latency, but sub-millisecond and resilient |

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| Cost-effective, simple, okay with data-loss risk | Sticky Sessions |
| Session data must survive server failure | Distributed Session (ElastiCache) |
| Even traffic distribution with ASG | Distributed Session |

---

## AUTO SCALING

### 11. Auto Scaling Groups (ASG)

| Thing | Explanation |
|---|---|
| SQS-based scaling | Can scale EC2 based on number of messages in an SQS queue |

**Scaling Types**

| Type | Predictable or Reactive? | Best for |
|---|---|---|
| Scheduled Scaling | Predictable | Known dates/times of high/low traffic |
| Target Tracking (Dynamic) | Reactive | Sudden, unpredictable spikes — "keep CPU at X%" |
| Predictive Scaling | Predictable (ML-based) | Cyclical patterns + slow-starting apps; saves money by avoiding overprovisioning |

**Suspend-Resume:** Temporarily pause scaling activities — useful during config changes/troubleshooting.

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| Scale based on queue backlog | ASG scaling on SQS |
| Known/predictable traffic pattern on specific days | Scheduled Scaling |
| Unpredictable spikes, keep metric at target % | Target Tracking |
| Cyclical/recurring traffic, slow-starting apps | Predictive Scaling |
| Pause scaling while troubleshooting | Suspend-Resume |

---

## DATABASES

### 12. Amazon RDS

| Thing | Explanation |
|---|---|
| Workload type | OLTP (small, fast transactions) |
| Storage Auto Scaling | Grows storage automatically, zero downtime |
| Migration | AWS DMS migrates on-prem DBs (e.g. Oracle) without code changes |

**Read Replicas**

| Thing | Explanation |
|---|---|
| Purpose | Performance — offload reads from primary |
| Region support | Multi-region supported |
| Creation | Takes a snapshot first; brief I/O pause during snapshot |
| Requirements | Automatic backups must be ON; avoid long-running transactions during creation |
| When to use | Performance, internal reporting, read-heavy scaling, serving reads if primary down (data may be stale), business reporting/data warehousing |

**Important distinction:** Read Replica = performance. Multi-AZ = disaster recovery.

**Other Notes**

| Thing | Explanation |
|---|---|
| Standby Instance (Multi-AZ) | Same AZ-specific region only |
| Secrets Manager | Protects RDS passwords, automatic rotation |
| ElastiCache for Redis | Speeds up RDS reads (e.g. gaming leaderboards) |
| Encrypt existing unencrypted RDS | Snapshot → encrypted copy of snapshot → restore from encrypted snapshot |

**Multi-AZ Deployment**

| Thing | Explanation |
|---|---|
| RPO | Less than 1 second |
| Region limit | Same region only — no cross-region Multi-AZ |

**RDS HA/DR Metrics**

| Feature | RPO | RTO |
|---|---|---|
| Multi-AZ | ~0 | 1–2 min |
| Read Replica promotion (in-region) | Minutes | <5 min |
| PITR (in-region) | ~5 min | Minutes–hours |
| PITR (cross-region) | 6–20 min | Minutes–hours |
| Snapshot restore | Hours | Minutes–hours |

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| Improve read performance | Read Replica |
| Disaster recovery, automatic failover, same region | Multi-AZ |
| Migrate on-prem DB without code changes | AWS DMS |
| Need replica across multiple regions | Read Replica (Multi-AZ can't) |
| Encrypt existing unencrypted RDS | Snapshot → encrypted copy → restore |

---

### 13. AWS Aurora

| Thing | Explanation |
|---|---|
| Compatibility | MySQL or PostgreSQL |
| Replication latency | Under 1 second |
| Auto Scaling for replicas | Adds/removes replicas to fix latency/capacity issues |

**Aurora Global Database (DR)**

| Thing | Explanation |
|---|---|
| Purpose | DR between two AWS regions |
| Performance impact | None on the primary |
| Bonus | Fast local reads in each region |
| RPO | 1 second |
| RTO | Less than 1 minute |

**Aurora Serverless:** Automatically starts/stops/scales capacity; no instance class to choose; best for infrequent/spiky usage.

**Aurora Read Replicas**

| Thing | Explanation |
|---|---|
| Purpose | Offload reads from primary |
| Max replicas | 15 per cluster |
| Failover | Automatic — Aurora promotes a replica if primary fails |

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| DR between two AWS regions, Aurora | Aurora Global Database |
| Fast regional failover (<1 min) | Aurora Global Database |
| Unpredictable/spiky usage, no capacity management | Aurora Serverless |
| Offload reads + need automatic failover | Aurora Read Replica |

**Don't confuse with RDS Multi-AZ:** RDS Multi-AZ = same region only. Aurora Global Database = spans multiple regions.

---

### 14. AWS Redshift

| Thing | Explanation |
|---|---|
| Purpose | Data warehousing |
| Workload type | OLAP (complex queries, big joins) — not OLTP |
| Data types | Structured + semi-structured (JSON) |
| Storage | Columnar — fast for analytical queries |
| Scale | Petabyte-scale |

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| Data warehouse, complex analytical queries | Redshift |
| OLAP, big joins across large tables | Redshift |
| Everyday app transactions | NOT Redshift → RDS/Aurora |

**Redshift vs Athena**

| Feature | Redshift | Athena |
|---|---|---|
| Data location | Loaded into Redshift | Stays in S3 |
| Best for | Frequent, heavy queries | Occasional/ad-hoc queries |
| Setup | Provision a cluster | No infrastructure |
| Cost | Pay for cluster | Pay per query |

---

### 15. Amazon DynamoDB

| Thing | Explanation |
|---|---|
| Database type | NoSQL — key-value/document |
| Performance | Millions of requests/sec, millisecond response |
| Data format | JSON-like documents |
| Max item size | 400 KB |
| Fully managed | No servers, auto-scales |

**On-Demand Capacity Mode**

| Best for | Unpredictable traffic, flash sales, large short spikes, new/complex-to-forecast apps, serverless pay-per-use, SaaS table-per-subscriber |

**VPC Endpoints for DynamoDB:** Lets resources access DynamoDB without public internet; needs a route table entry.

**TTL (Time to Live):** Auto-deletes items after a set time. Use cases: remove inactive data, archive to S3 via Streams+Lambda before deletion, comply with retention rules, stop monitoring old orders.

**Secondary Index:** Query by an attribute other than the primary key (e.g. Customer ID, Tracking ID).

**Minimal operational overhead (database) → DynamoDB**, not RDS.

**DAX (DynamoDB Accelerator):** Fully managed in-memory cache in front of DynamoDB — takes response time from milliseconds to microseconds.

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| JSON documents, key-value store | DynamoDB |
| Millions of req/sec, ms latency | DynamoDB |
| Unpredictable traffic, flash sale | On-Demand mode |
| EC2/Lambda needs private access, no internet | VPC Endpoint |
| Auto-delete old/expired items | TTL |
| Archive expiring items to S3 first | TTL + Streams + Lambda |
| Query by non-primary-key attribute | Secondary Index |
| Need even faster reads (microseconds) | DAX |
| Need complex joins | NOT DynamoDB → RDS/Aurora |

---

## SERVERLESS, MESSAGING & INTEGRATION

### 16. Amazon API Gateway

| Thing | Explanation |
|---|---|
| API types | REST, HTTP, WebSocket |
| Common pairing | Lambda (fully serverless) |
| Handles | Routing, auth (IAM/Cognito), throttling, caching, monitoring, versioning |

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| Create/manage REST APIs, no servers | API Gateway |
| Throttle/rate-limit API requests | API Gateway |
| Minimal overhead, serverless backend for API | API Gateway + Lambda |
| Real-time two-way comms (chat) | API Gateway WebSocket |

---

### 17. Serverless Microservices Architecture (Pattern)

**Frontend Layer:** S3 + CloudFront (static website hosting).

**Application Layer (3 combos, by overhead, lowest first):**

| Combo | Overhead |
|---|---|
| API Gateway + Lambda | Lowest |
| API Gateway/NLB + Fargate | Low-medium (serverless containers) |
| ALB + ECS (EC2 launch type) | Higher (manage EC2 instances) |

**DB Layer:**

| Option | Best For |
|---|---|
| DynamoDB | Key-value/JSON, minimal management |
| Aurora | Relational/SQL/joins |
| ElastiCache | Caching on top of either |

**Classic minimal-overhead architecture:**
```
User → CloudFront → S3 (frontend)
                  ↓
        API Gateway → Lambda → DynamoDB
```

---

### 18. Amazon SQS

**Standard Queues**

| Thing | Explanation |
|---|---|
| Delivery | At-least-once (duplicates possible) |
| Order | Best-effort |
| Throughput | High |

**FIFO Queues**

| Thing | Explanation |
|---|---|
| Delivery | Exactly-once, no duplicates |
| Order | Guaranteed |
| Throughput | Lower |

**SQS Temporary Queue Client:** Short-lived request-response messaging, uses virtual queues (no real queue create/delete overhead).

**Deduplication (FIFO):** Content-based deduplication, OR explicit Message Deduplication ID.

**Priority pattern:** No built-in priority — use two separate Standard queues, consumer checks high-priority queue first.

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| Decouple components | SQS |
| High throughput, duplicates ok | Standard Queue |
| Strict order, no duplicates | FIFO Queue |
| Avoid dropping/duplicating DB writes | SQS FIFO |
| Need to prioritize messages | Two separate queues |

**Don't confuse with:** SNS (pub/sub, fan-out to many) or Kinesis (streaming, multiple re-readable consumers).

---

### 19. Amazon Kinesis

| Thing | Explanation |
|---|---|
| Purpose | Real-time streaming data (clickstreams, sensor data) |
| Default retention | 24 hours, extendable to 7 days |
| Why extend retention | If destination (e.g. S3) isn't getting all data, gives time to retry |

**4 Kinesis Services**

| Service | Purpose |
|---|---|
| Kinesis Video Streams | Stream video from devices for analytics/ML |
| Kinesis Data Streams | Raw capture, GB/sec, you build the consumer |
| Kinesis Data Firehose | Auto-load streams into S3/Redshift/OpenSearch, near real-time, no custom consumer code |
| Kinesis Data Analytics | Run SQL or Apache Flink directly on a stream |

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| Real-time clickstream/sensor data, custom processing | Kinesis Data Streams |
| Auto-deliver streaming data to S3/Redshift | Kinesis Data Firehose |
| Run SQL/Flink on a stream | Kinesis Data Analytics |
| Stream video for ML | Kinesis Video Streams |

**Don't confuse with SQS:** SQS = one message, one consumer, deleted after read. Kinesis = stream, multiple consumers, retained for a window.

---

### 20. Amazon SNS

**Fanout Scenario:** One message published to an SNS topic is replicated and pushed to multiple endpoints (SQS, Lambda, Firehose, HTTP(S)) simultaneously — enables parallel async processing.

```
S3 Event → SNS Topic → fans out to: SQS / Lambda / Firehose / HTTP(S)
```

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| One event triggers multiple independent processes | SNS Fanout |
| Run multiple programs in parallel from one trigger | SNS Fanout |

**Classic combo:** SNS → fans out to multiple SQS queues (each gets buffering/retry benefits).

---

### 21. Amazon SES

| Thing | Explanation |
|---|---|
| Purpose | Send/receive email programmatically at scale |
| Security | Encryption, DKIM, SPF support |
| Use cases | Transactional emails, marketing, notifications, receiving email (with S3/Lambda) |

**Don't confuse with:** SNS (simple notifications, can include email as one channel among several, no templates/tracking) or WorkMail (full hosted business email/calendar).

---

## SECURITY & MONITORING

### 22. AWS Secrets Manager

| Thing | Explanation |
|---|---|
| Main idea | Securely stores passwords/API keys/tokens |
| Automatic rotation | Yes, built-in, including native RDS support |
| Used by | EC2, Lambda apps needing credentials at runtime |

**Secrets Manager vs Parameter Store**

| Feature | Secrets Manager | Parameter Store |
|---|---|---|
| Auto rotation | Yes | No (needs custom Lambda+EventBridge) |
| Cost | Paid | Free tier available |
| Best for | Passwords/credentials needing rotation | General config, non-rotating secrets |

---

### 23. Amazon Inspector

| Thing | Explanation |
|---|---|
| Scope | EC2 instances + container workloads only |
| Finds | Software vulnerabilities + unintended network exposure |

| Assessment | Needs Agent? | Checks |
|---|---|---|
| Host Assessment | Yes | Vulnerable packages, best-practice deviations |
| Network Assessment | No | Network exposure (e.g. unintended open ports) |

**Don't confuse with:** Trusted Advisor (broad account recommendations), GuardDuty (active threat detection), Config (compliance tracking).

---

### 24. Amazon GuardDuty

| Thing | Explanation |
|---|---|
| Main idea | Continuous threat detection using ML/anomaly detection |
| Detects | Cryptocurrency mining attacks, compromised instances, unusual API calls |
| No agents needed | Analyzes existing logs |

**Logs Analyzed**

| Log | Looks For |
|---|---|
| CloudTrail | Unusual API calls, unauthorized deployments |
| VPC Flow Logs | Unusual internal traffic, suspicious IPs |
| DNS Logs | Compromised instances exfiltrating data via DNS |

---

### 25. Amazon Macie

| Thing | Explanation |
|---|---|
| Scope | S3 only |
| Finds | Sensitive data (PII) using ML |

**Mental Model**

| Service | Question Answered | Scope |
|---|---|---|
| Inspector | Do I have exploitable vulnerabilities? | EC2/Containers |
| GuardDuty | Is someone attacking me right now? | Whole account (logs) |
| Macie | Is sensitive S3 data exposed? | S3 only |
| Config | Did configs change out of compliance? | Whole account |

---

### 26. AWS Shield

| Thing | Explanation |
|---|---|
| Purpose | DDoS protection |

| Feature | Shield Standard | Shield Advanced |
|---|---|---|
| Cost | Free, automatic | Paid |
| Layer coverage | Layer 3/4 | Layer 3/4 + 7 |
| Extra features | None | 24/7 DRT, diagnostics, cost protection |

**Common combo:** CloudFront + Shield + WAF.

---

### 27. AWS WAF

| Thing | Explanation |
|---|---|
| Purpose | Filters malicious web requests (Layer 7) — SQL injection, XSS, HTTP flooding |
| Geo restriction | Can block/allow by country |
| Rule evaluation order | WAF rules run BEFORE resource policies, IAM, Lambda authorizers, Cognito authorizers |

**Deploy on:** CloudFront, ALB, API Gateway, AppSync. **NOT supported on NLB** (Layer 4, no HTTP content to inspect).

**Don't confuse with:** Shield (DDoS volume), Security Groups/NACLs (network-level, no HTTP awareness).

---

### 28. Amazon CloudWatch

| Thing | Explanation |
|---|---|
| Main idea | Monitoring — metrics, logs, alarms |
| Default metrics | CPU, Network, Disk I/O |
| NOT default | Memory, disk space, swap usage — need CloudWatch Agent (e.g. SwapUtilization) |

**EC2 Auto-Recovery Alarm**

| Thing | Explanation |
|---|---|
| Triggers on | Instance status check failures (software/OS issue) |
| Does NOT trigger on | System status check failures (underlying hardware) alone |
| What recovery does | Moves instance to new hardware, keeps same ID/IPs |

---

### 29. AWS CloudTrail

| Thing | Explanation |
|---|---|
| Logs by default | Management events only |
| Extra cost | Data events, Insights events |

| Event Type | Logs | Default? |
|---|---|---|
| Management | Control-plane actions | Yes |
| Data | S3 object activity, Lambda invocations | No |
| Insights | Unusual API patterns | No |

**Protecting logs:** Dedicated centralized S3 bucket, log file integrity validation, SSE-KMS encryption (default is SSE-S3), S3 bucket policy.

**Sharing across accounts:** Create IAM role per account → attach read-only policy → other account's IAM user assumes role to retrieve logs.

**Don't confuse with:** CloudWatch (performance metrics) or Config (configuration change tracking).

---

## NETWORKING (VPC & CONNECTIVITY)

### 30. Amazon VPC

**Expanding IP capacity:** Cannot modify existing VPC/subnet CIDR. Options: add secondary CIDR block, OR create new VPC + migrate.

**Rules:** Can't disable IPv4; can have IPv4+IPv6 together but not IPv6-only.

**VPC Sharing:** Multiple accounts (same AWS Organization) share a VPC's subnets to launch resources (EC2, RDS, Redshift, Lambda) — centralizes networking, avoids duplicate NAT Gateways/VPNs.

**VPC Flow Logs:** Captures IP traffic info; sent to CloudWatch Logs or S3. Used for: monitoring traffic, diagnosing overly restrictive Security Groups, determining traffic direction.

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| VPC out of IPs, can't change CIDR | Add secondary CIDR block |
| Need a completely different IP range | New VPC + migrate |
| Multiple accounts, same Org, need shared network | VPC Sharing |
| Troubleshoot blocked traffic / SG rules | VPC Flow Logs |

---

### 31. NAT Gateway

| Thing | Explanation |
|---|---|
| Purpose | Lets private subnet instances reach internet outbound-only |
| Location | Must be in a public subnet |
| Resilience | Tied to a single AZ — if AZ fails, NAT Gateway fails |
| Fix | One NAT Gateway PER AZ for fault tolerance |

**Don't confuse with:** Internet Gateway (two-way access for public subnet resources) or NAT Instance (self-managed EC2-based alternative, AWS prefers NAT Gateway).

---

### 32. AWS Site-to-Site VPN

| Thing | Explanation |
|---|---|
| Setup | Immediate |
| Cost | Cheaper than Direct Connect |
| Max throughput per tunnel | 1.25 Gbps |
| Scale beyond limit | AWS Transit Gateway + ECMP routing + additional tunnels |

**VPN vs Direct Connect**

| Feature | VPN | Direct Connect |
|---|---|---|
| Connection | Public internet (encrypted) | Dedicated private line |
| Setup time | Immediate | Weeks/months |
| Cost | Cheaper | More expensive |
| Throughput | Limited (1.25 Gbps/tunnel) | Much higher |

**Common combo:** Direct Connect primary + VPN backup.

---

### 33. AWS Direct Connect

| Thing | Explanation |
|---|---|
| Main idea | Dedicated private connection, bypasses public internet |
| Data transfer cost | Lower than internet |

**Resiliency Levels**

| Level | Connections | Locations | Protects Against |
|---|---|---|---|
| Maximum Resiliency | Multiple, separate devices | More than one location | Device, connectivity, complete location failure |
| High Resiliency | One per location | Multiple locations | Device, fiber cut, complete location failure |

---

### 34. Multiple VPC Connection (Isolation Pattern)

**Scenario:** Multiple VPCs (Prod/Dev/Test) need to reach on-prem but must NOT share resources/communicate with each other.

**Why NOT Transit Gateway:** It's a hub — naturally enables VPC-to-VPC communication, which breaks the isolation requirement.

**Correct solution:** Direct Connect (shared physical backbone) + a SEPARATE VPN connection per VPC back to the data center. Each VPC reaches on-prem only, not each other.

**Exam Triggers**

| If the question says... | Pick this |
|---|---|
| Multiple VPCs to on-prem, must stay isolated | Direct Connect + separate VPN per VPC |
| Multiple VPCs to on-prem, sharing is fine | Transit Gateway |

---

## IDENTITY & ACCESS

### 35. AWS Organizations — `aws:PrincipalOrgID`

| Thing | Explanation |
|---|---|
| What it does | Condition key in resource-based policies (e.g. S3 bucket policy) restricting access to principals within your AWS Organization |
| Benefit | No need to list every account ID; new accounts automatically covered |

**Don't confuse with:** `aws:PrincipalAccount` (one specific account only), identity-based IAM policies (control what a user/role can do), SCPs (guardrails at Org/OU level).

---

## ANALYTICS

### 36. AWS Glue

| Thing | Explanation |
|---|---|
| Main idea | Fully managed, serverless ETL (Extract, Transform, Load) |
| Glue Crawler | Scans data sources (e.g. S3), auto-discovers schema |
| Glue Data Catalog | Central metadata repository, used by Athena/Redshift Spectrum |
| Glue Jobs | ETL scripts (Python/Scala), can be auto-generated |
| Glue Studio | Visual, no-code ETL builder |

**Typical workflow:**
```
Raw data in S3 → Glue Crawler → Glue Data Catalog → Glue Job (transform) → S3/Redshift → queried by Athena/Redshift
```

**Don't confuse with:** EMR (custom Hadoop/Spark clusters, more control), Athena (queries data, doesn't transform it), Kinesis Firehose (streaming data, not batch).

---

*End of guide — 36 services/topics covered. Send the next service to keep building this out.*
