# SSL Cheatsheet

```bash
# View single certificate
echo | openssl s_client -showcerts -servername  [gnupg.org](http://gnupg.org)  -connect  [gnupg.org:443](http://gnupg.org:443)  2>/dev/null | openssl x509 -inform pem -noout -text | tee output.log

openssl pkcs7 -print_certs -in old.p7b -out new.crt
# openssl pkcs7 -print_certs -in old.p7b -out new.cer


# generate RSA public/private key
openssl genrsa -des3 -out darvein.pem 2048
# export RSA public key
openssl rsa -in private.pem -outform PEM -pubout -out public.pem
# export RSA private key
openssl rsa -in private.pem -out private_unencrypted.pem -outform PEM


openssl s_client -connect  [www.google.com:443](http://www.google.com:443) 
ncat --ssl localhost 30001
rts crl newcerts private


# generating CA's keypair with RSA - DES
openssl genrsa -des3 -out private/root-ca.key 4096

# create CSR 
openssl req -new -key private/root-ca.key -out root-ca.csr -config ./openssl.cnf

# creating our signing certificate, 1 year
openssl ca  -config ./openssl.cnf -create_serial -out root-ca.crt -days 365 -keyfile private/root-ca.key -selfsign -infiles root-ca.csr
```

# SSL Installation basics

```bash
# testing SSL SNI 
openssl s_client -connect verrents.com:443 -showcerts -servername verrents.com 

# Show SSL CERT
openssl s_client -showcerts -connect alumni.hsbc.com:443 </dev/null

# Generate a CSR
mkdir ~/ssl; cd ~/ssl
openssl req -new -newkey rsa:2048 -nodes -keyout private.pem -out csr.pem

# Verify CSR
openssl req -noout -text -in test.com.csr
openssl req -in mycsr.csr -noout -text

# Check HTTPS cert of a domain
export THISHOST=app.avisare.com
openssl s_client -connect $THISHOST:443 -showcerts -servername $THISHOST

# Apply godaddy ssl cert on aws
aws iam upload-server-certificate --server-certificate-name www.domain.com --certificate-body file://public.pem --private-key file://private.pem --certificate-chain file://gd_bundle-g2-g1.crt


# decode der
openssl x509 -in certificate.der -inform der -text -noout

# transform der to pem and pem to der
openssl x509 -in cert.crt -outform der -out cert.der
openssl x509 -in cert.crt -inform der -outform pem -out cert.pem
```

```bash
# openssl verification of tls 1.2
openssl s_client -connect google.com:443 -tls1_2
```

# Daily openssl usage

```bash
openssl req -in mycsr.csr -noout -text	# inspect a CSR info

# Encrypt and decrypt
openssl enc -aes256 -k P3NT35T3RL48 -in /tmp/backup.tgz  -out /tmp/backup.tgz.enc
openssl enc -aes256 -d  -in /tmp/backup.tgz.enc -out /tmp/backup.tgz

# Check domains for a 443 site
true | openssl s_client -connect nextbrave.com:443 2>/dev/null | openssl x509 -noout -text | perl -l -0777 -ne '@names=/\bDNS:([^\s,]+)/g; print join("\n", sort @names);'

# Check a certificate
openssl x509 -in server.crt -text -noout
```
