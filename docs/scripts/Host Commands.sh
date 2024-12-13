http://unix:/run/pms_backend_gunicorn_janakpurdham.sock

sudo nano /etc/systemd/system/pms_backend_gunicorn_janakpurdham.socket
sudo nano /etc/systemd/system/pms_backend_gunicorn_janakpurdham.service


sudo systemctl start pms_backend_gunicorn_janakpurdham.socket
sudo systemctl enable pms_backend_gunicorn_janakpurdham.socket
sudo systemctl status pms_backend_gunicorn_janakpurdham.socket
sudo file /run/pms_backend_gunicorn_janakpurdham.sock
sudo journalctl -u pms_backend_gunicorn_janakpurdham.socket
curl --unix-socket /run/pms_backend_gunicorn_janakpurdham.sock localhost
sudo systemctl daemon-reload
sudo systemctl restart pms_backend_gunicorn_janakpurdham


sudo nano /etc/systemd/system/pms_backend_gunicorn_rishingmun.socket
sudo nano /etc/systemd/system/pms_backend_gunicorn_rishingmun.service


sudo systemctl start pms_backend_gunicorn_rishingmun.socket
sudo systemctl enable pms_backend_gunicorn_rishingmun.socket
sudo systemctl status pms_backend_gunicorn_rishingmun.socket
sudo file /run/pms_backend_gunicorn_rishingmun.sock
sudo journalctl -u pms_backend_gunicorn_rishingmun.socket
curl --unix-socket /run/pms_backend_gunicorn_rishingmun.sock localhost
sudo systemctl daemon-reload
sudo systemctl restart pms_backend_gunicorn_rishingmun