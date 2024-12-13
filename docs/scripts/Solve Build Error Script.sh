echo "Fixing KMC Frontend repo"
cd /home/pms/pms-frontends/kmc
rm -rf node_modules
rm -rf package-lock.json
npm install --force
echo "KMC Frontend Fix Complete"

echo "Fixing Janakpurdham SMC Frontend repo"
cd /home/pms/pms-frontends/jsmc
rm -rf node_modules
rm -rf package-lock.json
npm install --force
echo "Janakpurdham SMC Frontend Fix Complete"

echo "Fixing Rishing Municipality Frontend repo"
cd /home/pms/pms-frontends/rishimun
rm -rf node_modules
rm -rf package-lock.json
npm install --force
echo "Rishing Municipality Frontend Fix Complete"

echo -e "Would you like to update the frontends now? (y/n) \c"
read -r updateFrontends

if [ "$updateFrontends" = "y" ]; then
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/frontend_ssh_key
    
    echo "Updating KMC Frontend"
    cd /home/pms/pms-frontends/kmc
    npm run build
    echo "KMC Frontend Updated"
    
    echo "Updating JSMC Frontend"
    cd /home/pms/pms-frontends/jsmc
    npm run build
    echo "JSMC Frontend Updated"
    
    echo "Updating Rishimun Frontend"
    cd /home/pms/pms-frontends/rishimun
    npm run build
    echo "Rishimun Frontend Updated"
    
    echo "Restarting PM2"
    pm2 restart all
    echo "PM2 Restarted"
else
    echo "Frontend update skipped"
fi

echo "Fixing Complete. Exiting the script..."