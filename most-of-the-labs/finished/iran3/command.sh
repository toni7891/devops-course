# name volume
docker volume create postgress-data

docker run -d --name postgres-db --network postgres-network -p 5432:5432 -v postgress-data:/var/lib/postgressql/data -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin123 -e POSTGRES_DB=company postgres

#username 

# network
# auth
# database


