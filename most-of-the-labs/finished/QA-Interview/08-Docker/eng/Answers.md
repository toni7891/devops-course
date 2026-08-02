# Docker Interview Answers

**Q1. What is a Docker image?**
A blueprint for creating containers — it includes code, libraries, and settings needed to run an application in an isolated environment.

**Q2. What is a Docker host?**
The machine where Docker is installed. It runs and manages containers, whether on a local machine, VM, or cloud instance.

**Q3. How is a Docker client different from a Docker daemon?**
The client sends commands (e.g. `docker run`); the daemon receives and executes them. They can run on the same or different machines.

**Q4. What is Docker networking? How do you create bridge/overlay networks?**
Networking lets containers communicate. Bridge (same host): `docker network create -d bridge my-bridge-network`. Overlay (cross-host): `docker network create --scope=swarm -d overlay my-overlay`.

**Q5. How does Docker bridge networking work?**
The default network mode. Each container on the same host gets a unique IP and can communicate directly with other containers on the bridge.

**Q6. What is a Dockerfile?**
A script of build instructions. It defines base image, working directory, file copies, dependency installs, exposed ports, and startup command — each step creates a layer.

**Q7. What is Docker Compose? How does it differ from Dockerfile?**
Compose manages multi-container apps via a YAML file. A Dockerfile builds one image; Compose spins up and connects multiple containers together.

**Q8. Why use volumes in Docker?**
Volumes store data outside the container so it persists after the container is removed. They're easier to back up and can be shared across containers.

**Q9. What are bind mounts? Why prefer volumes?**
Bind mounts link a host path into the container. Volumes are preferred because they're OS-independent, easier to manage, and more secure.

**Q10. What is Docker Swarm?**
Docker's built-in orchestration tool. It manages a cluster of Docker nodes, enabling load balancing, scaling, and high availability.

**Q11. Can Docker Swarm autoscale?**
Not natively. You can set up autoscaling manually by integrating Prometheus for monitoring and triggering `docker service scale` commands.

**Q12. How do you scale services with Docker Compose?**
Use the `--scale` flag: `docker-compose up --scale web=3` runs 3 instances of the `web` service.

**Q13. Can containers restart automatically?**
Yes. Default policy is `no` (no restart). Use `--restart=always` to restart a container whenever it stops.

**Q14. What is the Docker container lifecycle?**
Create → Run → Pause → Stop → Delete. A container can be stopped by a command, completion of its process, or an OOM kill.

**Q15. What is a Docker image repository?**
A storage system for Docker images with version tags. Docker Hub is the most popular; alternatives include Amazon ECR and GitHub Container Registry.

**Q16. Name three container security best practices.**
1. Use minimal base images (e.g. Alpine).
2. Limit syscalls with Seccomp.
3. Use Docker secrets for sensitive data instead of environment variables.

**Q17. Why do containers need health checks?**
To detect when a running container is no longer functioning correctly (e.g. stuck or not responding), so it can be restarted or replaced.

**Q18. What are dangling images? How do you remove them?**
Unused image layers with no tag, wasting disk space. Find them: `docker images -f dangling=true`. Remove them: `docker image prune -f`.

**Q19. What is the difference between Docker and Kubernetes?**
Docker builds and runs individual containers. Kubernetes orchestrates many containers across a cluster with auto-scaling, load balancing, and self-healing.

**Q20. Docker Swarm vs Kubernetes?**
Swarm is simpler and good for small setups. Kubernetes is more powerful, with better self-healing, monitoring, and support for large-scale deployments.

**Q21. How does Kubernetes manage large numbers of containers?**
Through intelligent scheduling, resource allocation across nodes, and automatic scaling based on workload — plus self-healing when containers fail.

**Q22. What is a Kubernetes Pod?**
The smallest deployable unit in Kubernetes. A Pod groups one or more containers that share network and storage, unlike standalone containers which are isolated.

**Q23. How do you manage secrets in Docker and Kubernetes?**
Docker: Use Docker secrets — encrypted and only accessible at runtime. Kubernetes: Use Secret objects, mounted as volumes or environment variables.

**Q24. How do you reduce a large Maven Docker image size?**
Add a `.dockerignore` file to exclude unnecessary files, and use multi-stage builds — compile in one stage, copy only the final artifact to a lightweight runtime image.

**Q25. How do you push Docker images to Docker Hub via Jenkins?**
Set up a Jenkins pipeline with a `Jenkinsfile` that builds the image, logs into Docker Hub using stored credentials, and pushes the image automatically.

**Q26. How do you migrate a WordPress Docker container without data loss?**
1. Backup data: `docker cp <container>:/var/www/html ./backup`
2. Transfer to new server: `scp`
3. Deploy containers on new server
4. Restore volume data before starting
