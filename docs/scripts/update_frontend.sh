echo "Adding SSH Key for pulling updates"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/frontend_ssh_key
cd pms_frontend
echo "Pulling updates from Github"
git pull origin main
echo "Building frontend"
npm run build
echo "Removing old build"
sudo rm -r /var/www/pms.lgerp.org/html/*
echo "Moving build to host"
sudo mv dist/* /var/www/pms.lgerp.org/html/
