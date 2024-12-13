#!/bin/bash

# Array of frontend directories
declare -A frontend_directories=(
    ["lmc"]="home/pms/pms_frontend"
    ["kmc"]="/home/pms/pms-frontends/kmc"
    ["jsmc"]="/home/pms/pms-frontends/jsmc"
    ["rishimun"]="/home/pms/pms-frontends/rishimun"
    ["mithila"]="/home/pms/pms-frontends/mithila"
)

# Array of frontend server names
declare -A frontend_server_names=(
    ["lmc"]="Lalitpur Metropolitan City"
    ["kmc"]="Kathmandu Metropolitan City"
    ["jsmc"]="Janakpur Sub-Metropolitan City"
    ["rishimun"]="Rishing Municipality"
    ["mithila"]="Mithila Municipality"
)

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/frontend_ssh_key


function is_package_json_updated() {
    # Perform a git pull and capture the output
    git_pull_output=$(git pull origin main)
    
    # Check if there are updates
    if [[ $git_pull_output == *"Already up to date"* ]]; then
        echo "No updates found."
        return 1
    else
        # Check if package.json is modified
        if git diff --name-only HEAD@{1} | grep -q "package.json"; then
            echo "Package.json has been updated."
            return 0
        else
            echo "Other files have been updated, but package.json is unchanged."
            return 1
        fi
    fi
}

echo "Updating Frontends"
for key in "${!frontend_directories[@]}"; do
    echo "Updating ${frontend_server_names[$key]} Frontend"
    cd ${frontend_directories[$key]}
    git stash
    git stash drop
    # Call the function
    is_package_json_updated
    # Capture the return value
    result=$?
    # Use the result as needed
    if [ $result -eq 0 ]; then
        echo "Looks like npm packages were updated in the project. Removing node_modules and reinstalling.."
        rm -rf node_modules
        rm -rf package-lock.json
        npm install --force
    else
        echo "No pckages were updated. Running the build command."
    fi
    npm run build
    echo "${frontend_server_names[$key]} Frontend Updated"
done
echo "Frontends Updated"


echo -e "Would you like to update the frontends now? (y/n) \c"
read -r updateFrontends

if [ "$updateFrontends" = "y" ]; then
    echo "Restarting PM2"
    pm2 restart all
    echo "PM2 Restarted"
else
    echo "Frontend update skipped"
fi