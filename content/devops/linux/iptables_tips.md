# IPTables cheatsheet

```bash
## Centos 7 iptables
systemctl stop firewalld
systemctl mask firewalld
systemctl enable iptables

yum install iptables-services

systemctl enable iptables
systemctl [stop|start|restart] iptables
chkconfig --level 345 iptables on

iptables -L -n -v
iptables -F
service iptables save
iptables-save

## FLUSH de reglas iptables -F
iptables -X
iptables -Z
iptables -t nat -F
iptables -L -n -v

## FLush rules on centos
cat /etc/sysconfig/iptables
iptables -F
iptables -L 
service iptables save
service iptables stop
service iptables start
cat /etc/sysconfig/iptables
iptables -L



## Establecemos politica por defecto
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -t nat -P PREROUTING ACCEPT iptables -t nat -P POSTROUTING ACCEPT

## Empezamos a filtrar
# El localhost se deja (por ejemplo conexiones locales a mysql)
/sbin/iptables -A INPUT -i lo -j ACCEPT

# A nuestra IP le dejamos todo
iptables -A INPUT -s 195.65.34.234 -j ACCEPT

# A un colega le dejamos entrar al mysql para que mantenga la BBDD
iptables -A INPUT -s 231.45.134.23 -p tcp --dport 3306 -j ACCEPT

# A un dise√É¬±ador le dejamos usar el FTP
iptables -A INPUT -s 80.37.45.194 -p tcp -dport 20:21 -j ACCEPT

# El puerto 80 de www debe estar abierto, es un servidor web.
iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Y el resto, lo cerramos
iptables -A INPUT -p tcp --dport 20:21 -j DROP
iptables -A INPUT -p tcp --dport 3306 -j DROP
iptables -A INPUT -p tcp --dport 22 -j DROP
iptables -A INPUT -p tcp --dport 10000 -j DROP

# Cerramos el rango de puerto bien conocido
iptables -A INPUT -s 0.0.0.0/0 -p tcp -dport 1:1024 -j DROP
iptables -A INPUT -s 0.0.0.0/0 -p udp -dport 1:1024 -j DROP

# Aceptamos que vayan a puertos 80
iptables -A FORWARD -s 192.168.10.0/24 -i eth1 -p tcp --dport 80 -j ACCEPT
# Aceptamos que vayan a puertos https
iptables -A FORWARD -s 192.168.10.0/24 -i eth1 -p tcp --dport 443 -j ACCEPT

# Aceptamos que consulten los DNS
iptables -A FORWARD -s 192.168.10.0/24 -i eth1 -p tcp --dport 53 -j ACCEPT
iptables -A FORWARD -s 192.168.10.0/24 -i eth1 -p udp --dport 53 -j ACCEPT


# EXAMPLES
# --------------------------------------------------

iptables -A INPUT A -p tcp --dport PORT_NUMBER -j DROP # close port
iptables -A INPUT -s IP_ADDRESS -j DROP # ban ip address





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SSH Access
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
iptables -A INPUT -p tcp -s 72.232.194.162 --dport 22 -j ACCEPTs
iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --set --name ssh --rsource
iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent ! --rcheck --seconds 60 --hitcount 4 --name ssh --rsource -j ACCEPT

```

## Stopping a DDOS

```bash
#!/bin/bash

LIMIT_CONN=300
#SLACK_WEBHOOK_URL=https://hooks.slack.com/services/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
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/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

netstat -ntu|awk '{print $5}'|cut -d: -f1 -s|sort|uniq -c|sort -nk1 -r | head -n 5 | sed -e 's/^[[:space:]]*//' | while read -r line
do
        hits=`echo $line | awk '{print $1}'`
        ipaddr=`echo $line | awk '{print $2}'`

        if (( $hits > $LIMIT_CONN )); then
                # ban
                iptables -A INPUT -s $ipaddr/32 -j DROP
                iptables -A OUTPUT -s $ipaddr/32 -j DROP
                iptables -A INPUT -s $ipaddr/32 -j REJECT --reject-with tcp-reset
                route add $ipaddr reject

                # notify
                message="Blacklisted ${ipaddr}/32 as it had ${hits} concurrent connections in the past minute"
                curl -X POST -H 'Content-type: application/json' --data "{\"text\":\"$message\"}" $SLACK_WEBHOOK_URL
                echo $message

        fi
done
```
