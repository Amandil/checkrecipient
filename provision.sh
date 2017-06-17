
apt update

# Dev env set-up
apt -y install python3 python3-pip
pip3 install django psycopg2

apt -y install docker.io postgresql-client
docker run --name django-postgres -p 5432:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -d postgres
export PGPASSWORD=password
createdb -h localhost -p 5432 -U user checkrecipient
