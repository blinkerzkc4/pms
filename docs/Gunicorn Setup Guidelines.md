# Create systemd Socket and Service files for Gunicorn

## Create a systemd socket file

To create socket file

```shell
nano /etc/systemd/system/pms_backend_gunicorn.socket
```

Add the contents from [pms_backend_gunicorn.socket](../configs/pms_backend_gunicorn.socket) file.

## Create a systemd service file

To create service file

```shell
nano /etc/systemd/system/pms_backend_gunicorn.service
```

Add the contents from [pms_backend_gunicorn.service](../configs/pms_backend_gunicorn.service) file.

# Start and enable Gunicorn Socket

Start gunicorn with the following command

```shell
systemctl start pms_backend_gunicorn.socket
systemctl enable pms_backend_gunicorn.socket
```

# Checking the Gunicorn Socket file

To check status of gunicorn socket

```shell
systemctl status pms_backend_gunicorn.socket
```

To check existence of `gunicorn.sock` file

```shell
file /run/pms_backend_gunicorn.sock
```

To check the logs of gunicorn socket

```shell
journalctl -u pms_backend_gunicorn.socket
```

# Starting the Gunicorn Service

To check the status of gunicorn

```shell
systemctl status pms_backend_gunicorn
```

To test socket activation

```shell
curl --unix-socket /run/pms_backend_gunicorn.sock localhost
```

If `gunicorn.service` is changed, run this command to reload gunicorn

```shell
sudo systemctl daemon-reload
sudo systemctl restart pms_backend_gunicorn
```
