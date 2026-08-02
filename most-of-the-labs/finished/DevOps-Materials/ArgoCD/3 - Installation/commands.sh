helm repo add argo https://argoproj.github.io/argo-helm

helm repo update

helm search repo argo/argo-cd --versions

kubectl create namespace argocd

kubectl apply -f .

kubectl get namespaces

helm upgrade argocd argo/argo-cd \
  --version 8.6.0 \
  --install \
  --namespace argocd \
  --create-namespace