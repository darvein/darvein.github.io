# Wordpress

# Content

## Installation

Given an Ubuntu 22.04 Machine

```bash
sudo apt update 
sudo apt-get upgrade -y
sudo apt install -f php-fpm nfs-kernel-server nginx php-mysql
sudo apt install -f php8.1-mysql php8.1-mbstring php8.1-xml php8.1-curl
sudo apt install -f memcached libmemcached-tools -y
```

Check the nginx config:

```nginx
client_max_body_size 50M;

server {
    listen 80;
    listen [::]:80;
    root /var/www/acme.com/html;
    server_name _;

    index index.php;
    charset utf-8;
    access_log /var/log/nginx/wordpress_access.log;
    error_log /var/log/nginx/wordpress_error.log;

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass unix:/var/run/php8.1-fpm-wordpress-site.sock;
        fastcgi_index index.php;
        include fastcgi.conf;
        proxy_connect_timeout      3600;
        proxy_send_timeout         180;
        proxy_read_timeout         180;
    }

    location ~ /\.ht {
        deny all;
    }

    location ~ \.(eot|ttf|otf|woff)$ {
      add_header Access-Control-Allow-Origin *;
    }
}
```

Create php fpm profile:

```bash
vim /etc/php/8.1/fpm/pool.d/wordpress.conf

[wordpress_site]
user = www-data
group = www-data
listen = /var/run/php8.1-fpm-wordpress-site.sock
listen.owner = www-data
listen.group = www-data
php_admin_value[disable_functions] = exec,passthru,shell_exec,system
php_admin_flag[allow_url_fopen] = off
; Choose how the process manager will control the number of child processes.
pm = dynamic
pm.max_children = 75
pm.start_servers = 10
pm.min_spare_servers = 5
pm.max_spare_servers = 20
pm.process_idle_timeout = 10s
;upload_max_filesize = 50M
;post_max_size = 50M
```

Modify fpm:

```bash
sudo sed -i 's/upload_max_filesize = 2M/upload_max_filesize = 64M/g' /etc/php/8.1/fpm/php.ini
sudo sed -i 's/post_max_size = 8M/post_max_size = 128M/g' /etc/php/8.1/fpm/php.ini
```

Restart services:

```bash
sudo nginx -t
sudo systemctl enable nginx.service
sudo systemctl enable php8.1-fpm.service

sudo systemctl restart nginx.service
sudo systemctl restart php8.1-fpm.service
```

Install wordpress

```bash
wget https://wordpress.org/latest.tar.gz
tar -xzvf latest.tar.gz
```

Post configurations

```bash
# On wp-config.php allow web upload of zip files
define('FS_METHOD', 'direct');
```
