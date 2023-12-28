# Tcpdump

### tcpdump sniff on docker containers

- Check first the container ip address: `docker inspect $container`
- Get the interface network `ifconfig | less`
- Then TCPDump it:

```bash
# This is an nginx container
sudo tcpdump -i br-11a73f6ac535 -A -p -s 0 -l -vv -nn 'host 172.22.0.50'

# GET|POST packets
sudo tcpdump -i br-11a73f6ac535 -A -p -s 0 -l -vv -nn 'tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420'

# Receive on django
sudo tcpdump -i br-11a73f6ac535 -A -p -l -vvvs 1500 -nn -SX 'src 172.22.0.17'
sudo tcpdump -i br-11a73f6ac535 -A -p -l -vvvvs 1500 -nn 'dst 172.22.0.50'
sudo tcpdump -i br-11a73f6ac535 -A -p -l -vvvvs 1500 -nn 'src 172.22.0.17 and dst 172.22.0.50'

# Bind the container network
docker run -it --rm --net container:nginx-ca-qa nicolaka/netshoot tcpdump -A -p -l -vvvvs 1500 -nn 'dst 172.22.0.50'
docker run -it --rm --net container:nginx nicolaka/netshoot tcpdump -A -p -l -vvvvs 1500 -nn 'dst 172.20.1.102'
```
