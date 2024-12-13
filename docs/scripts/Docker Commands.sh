sudo docker build -t pms-shangrila-backend .
sudo docker images
sudo docker network create pms-shangrila-postgres-network
sudo systemctl stop postgresql-14
sudo docker run --name shangrila-postgres -p 5432:5432 -e POSTGRES_USER=yojana_db_user -e POSTGRES_PASSWORD=YojanaDatabasePassword321 --network pms-shangrila-postgres-network -d postgres
sudo docker ps
# interactive bash session within postgres container.
sudo docker exec -it shangrila-postgres bash
psql -U yojana_db_user
CREATE DATABASE yojana_db OWNER yojana_db_user;
# To exit use:
\q
exit
# Running the container
sudo docker run --name pms-shangrila-backend-app -p 8000:8000 --network pms-shangrila-postgres-network -d pms-shangrila-backend
sudo docker ps
# Running migrations
sudo docker exec -it pms-shangrila-backend-app python manage.py migrate

# Restart command
sudo docker exec -t shangrila-postgres pg_dumpall -c -U postgres > backup/dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
sudo docker build -t pms-shangrila-backend .
sudo docker stop pms-shangrila-backend-app
sudo docker rm pms-shangrila-backend-app
sudo docker run --name pms-shangrila-backend-app -p 8000:8000 --network pms-shangrila-postgres-network -d pms-shangrila-backend
sudo docker exec -it pms-shangrila-backend-app python manage.py migrate
sudo docker system prune

# Backup Docker Database
sudo docker exec -t shangrila-postgres pg_dumpall -c -U postgres > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql