# Variables:
DATABASE_BACKUP=/home/pms/backup
BACKEND_BASE_DIR=/home/pms/pms-backends/kmc
GUNICORN_SERVICE_NAME=pms_backend_gunicorn_kmc


echo "Updating the backend..."
# cd $DATABASE_BACKUP
# echo -e "Backing up the database...\nPlease enter the database password when prompted."
# current_date_time=$(date)
# pg_dump -d yojana_db -h 127.0.0.1 -U yojana_db_user -W > "Yojana Backup - $current_date_time.sql"
# echo "Backup complete."
cd $BACKEND_BASE_DIR
echo "Running the SSH Agent and adding the SSH key..."
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/backend_ssh_key
echo "Pulling changes from the repository..."
git pull origin main
echo "Migrating the database..."
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "Restarting the backend gunicorn service"
sudo systemctl restart $GUNICORN_SERVICE_NAME
deactivate
cd
echo "Backend system has been updated"