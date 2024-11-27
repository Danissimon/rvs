curl -X 'POST' \
  'http://localhost/increment/?value=9' \
  -H 'accept: application/json' \
  -d ''


nginx.conf:
server {
    listen 80;
    server_name localhost; 

    location / {
        proxy_pass http://127.0.0.1:8000; 
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

