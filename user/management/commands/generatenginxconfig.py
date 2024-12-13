import os

from django.conf import settings
from django.core.management.base import BaseCommand

from user.models import Client


class Command(BaseCommand):
    help = "Command to generate the nginx config file of the clients."

    def handle(self, *args, **options):
        self.stdout.write("Generating nginx config file of the clients...")
        nginx_config_file = os.path.join(settings.CONFIGS_DIR, "yojana_nginx.conf")
        domains_list = (
            " ".join(list(Client.objects.active().values_list("subdomain", flat=True)))
            + f" {settings.SUPERUSER_DOMAIN}"
        )

        nginx_config = (
            "map $http_upgrade $connection_upgrade {{\n"
            "    default         upgrade;\n"
            "    ''              close;\n"
            "}}\n"
            "\n"
            "server {{\n"
            "        listen 80;\n"
            "        listen 443;\n"
            "        client_max_body_size 4G;\n"
            "        server_name {domains_list};\n"
            "\n"
            "        location / {{\n"
            "                proxy_read_timeout 300;\n"
            "                proxy_connect_timeout 300;\n"
            "                proxy_send_timeout 300; \n"
            "                proxy_pass         {frontend_internal_url};\n"
            "                proxy_http_version  1.1;\n"
            "                proxy_set_header    Upgrade     $http_upgrade;\n"
            "                proxy_set_header    Connection  $connection_upgrade;\n"
            "        }}\n"
            "\n"
            "        location /static/ {{\n"
            "                root /var/www/data;\n"
            "        }}\n"
            "\n"
            "        location /media/ {{\n"
            "                root /var/www/data;\n"
            "        }}\n"
            "\n"
            "        location /api/ {{\n"
            "                proxy_read_timeout 300;\n"
            "                proxy_connect_timeout 300;\n"
            "                proxy_send_timeout 300;\n"
            "                send_timeout 300;\n"
            "                include proxy_params;\n"
            "                proxy_pass http://{gunicorn_socket_url};\n"
            "         }}\n"
            "\n"
            "        location /ws/ {{\n"
            "            proxy_set_header Host               $http_host;\n"
            "            proxy_set_header X-Real-IP          $remote_addr;\n"
            "            proxy_set_header X-Forwarded-For    $proxy_add_x_forwarded_for;\n"
            "            proxy_set_header X-Forwarded-Host   $server_name;\n"
            "            proxy_set_header X-Forwarded-Proto  $scheme;\n"
            "            proxy_set_header X-Url-Scheme       $scheme;\n"
            "            proxy_redirect off;\n"
            "\n"
            "            proxy_http_version 1.1;\n"
            "            proxy_set_header Upgrade $http_upgrade;\n"
            "            proxy_set_header Connection $connection_upgrade;\n"
            "\n"
            "            proxy_pass http://{websocket_unix_url};\n"
            "        }}\n"
            "        location /error-log/ {{\n"
            "                include proxy_params;\n"
            "                proxy_pass http://{gunicorn_socket_url};\n"
            "        }}\n"
            "\n"
            "        location /admin/ {{\n"
            "                proxy_read_timeout 300;\n"
            "                proxy_connect_timeout 300;\n"
            "                proxy_send_timeout 300; \n"
            "                include proxy_params;\n"
            "                proxy_pass http://{gunicorn_socket_url};\n"
            "        }}\n"
            "\n"
            "        location /redoc/ {{\n"
            "                include proxy_params;\n"
            "                proxy_pass http://{gunicorn_socket_url};\n"
            "        }}\n"
            "}}"
        ).format(
            domains_list=domains_list,
            frontend_internal_url=settings.FRONTEND_INTERNAL_URL,
            gunicorn_socket_url=settings.GUNICORN_SOCKET_URL,
            websocket_unix_url=settings.WEBSOCKET_UNIX_URL,
        )
        with open(nginx_config_file, "w") as f:
            f.write(nginx_config)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully generated nginx config file of the clients at {nginx_config_file}."
            )
        )
