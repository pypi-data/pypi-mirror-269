# Using Nginx as reverse proxy

As Argos has no authentication mechanism for the front-end, you need to protect some routes with HTTP authentication.

To do so on Debian, install `apache2-utils` then create a file containing the wanted credentials:
```bash
htpasswd -c /etc/nginx/argos.passwd argos_admin
```

You can then use this file to protect the front-end’s routes:
```{literalinclude} ../../conf/nginx.conf
---
caption: /etc/nginx/sites-available/argos.example.org
---
```
