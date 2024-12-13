# Variables:
BACKEND_BASE_DIR=/home/pms/projects/pms-backend
GUNICORN_SERVICE_NAME=pms_core_backend_gunicorn

cd $BACKEND_BASE_DIR
source venv/bin/activate
echo "Generating Config Files"
python manage.py generateconfigs
echo "Migrating Database"
python manage.py migrateall
echo "Updating Changes to the clients"
python manage.py refreshserver
echo "Updating the Nginx Configurations"
sudo cp pms_system/configs/yojana_nginx.conf /etc/nginx/sites-available/yojana_core_nginx.conf
echo "Restarting the backend server"
sudo systemctl restart $GUNICORN_SERVICE_NAME
echo "Restarting the Nginx Server"
sudo systemctl restart nginx
deactivate