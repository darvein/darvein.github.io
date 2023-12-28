# Nginx and certbot

```bash
sudo apt update
sudo apt install -f certbot python3-certbot-nginx nginx

sudo certbot --nginx -d acme.net -d www.acme.net

sudo vim /etc/nginx/sites-available/acme.net

#Successfully received certificate.
#Certificate is saved at: /etc/letsencrypt/live/acme.net/fullchain.pem
#Key is saved at:         /etc/letsencrypt/live/acme.net/privkey.pem

sudo crontab -e
 0 1 * * * /usr/bin/certbot renew --quiet
```

Nginx config:

```nginx
client_max_body_size 100M;
# Enable gzip compression
#gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css text/xml application/json application/javascript application/rss+xml application/atom+xml image/svg+xml;

# Cache settings
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;
proxy_cache_key "$scheme$request_method$host$request_uri";

server {
    listen 80;
    server_name acme.net www.acme.net acme.nextbrave.com acme.org acme.xyz www.acme.org www.acme.xyz;
    return 301 https://www.acme.net$request_uri;
}

server {
    listen 443 ssl;
    server_name acme.net;

    ssl_certificate /etc/letsencrypt/live/acme.net/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/acme.net/privkey.pem;

    return 301 https://www.acme.net$request_uri;
}

server {
    listen 443 ssl;
    server_name www.acme.net;

    ssl_certificate /etc/letsencrypt/live/acme.net/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/acme.net/privkey.pem;

    root /var/www/acme.net/html;
    index index.html;

    # Enable caching
    location ~* \.(jpg|jpeg|gif|png|css|js|ico|svg|woff|woff2|ttf|otf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
    location / {
        try_files $uri $uri/ =404;
    }
    location ~ ^/(p8|p82) {
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/drvsecret;
        try_files $uri $uri/ =404;
    }
}
```

```bash
sudo mkdir -p /var/www/acme.net/html
sudo ln -s /etc/nginx/sites-available/acme.net /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl reload nginx
```

### Setup permissions for rsync of html

```bash
sudo groupadd web
sudo usermod -aG web ubuntu
sudo usermod -aG web www-data
sudo chown -R ubuntu:web /var/www/yourdomain.com/html
sudo chmod -R 2775 /var/www/yourdomain.com/html
```

### Protect directories

```bash
sudo apt install -y apache2-utils
sudo htpasswd -c /etc/nginx/drvsecret drv

# Adding this to the nginx config
location ~ ^/(p8|p82) {
    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/drvsecret;
    try_files $uri $uri/ =404;
}

sudo nginx -t
sudo systemctl reload nginx
```
