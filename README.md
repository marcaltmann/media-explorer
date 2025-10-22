Media Explorer
================

Research and presentation software for media resources
------------------------------------------------------



Docker for development/staging environment
------------------------------------------

Create self-signed SSL certificates:

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./certs/nginx.key -out ./certs/nginx.crt
```
