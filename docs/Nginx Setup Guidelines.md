# Create a new server block

Create a new server block for the application with the following command.

```shell
    sudo nano /etc/nginx/sites-available/pms_backend
```

Add the contents from [pms_backend_server_block](../configs/pms_backend_server_block) file.

Create a symlink for the file with the following command

```shell
ln -s /etc/nginx/sites-available/pms_backend /etc/nginx/sites-enabled
```

To test the nginx configuration, run the following command

```shell
nginx -t
```

Restart nginx with the following command

```shell
systemctl restart nginx
```

Remove the old port and enable port for nginx with the following command

```shell
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
```
