helm list

helm install my-release bitnami/wordpress \
  --set "mariadb.auth.rootPassword=myawsomepassword" \
  --set "mariadb.auth.password=myuserpassword"

# Creation of a secret with the credentials
kubectl create secret generic custom-wp-credentials \
  --from-literal=wordpress-username=lirone \
  --from-literal=wordpress-password=lironepassword

# Using the custom values file to set the credentials and replica count
helm install my-release bitnami/wordpress -f custom-values.yaml