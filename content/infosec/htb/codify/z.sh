curl -s 'http://codify.htb:3000/run' \
	-X POST \
	-H 'Referer: http://codify.htb/editor' \
	-H 'Content-Type: application/json' \
	--data-raw '{"code":"dmFyIGZvbz0xOwpjb25zb2xlLmxvZyhmb28pOw=="}'

# Result
# {"output":"1\r\n"}

# What is that `code` b64?:
# echo "dmFyIGZvbz0xOwpjb25zb2xlLmxvZyhmb28pOw==" | base64 -d
# var foo=1;
# console.log(foo);
