docker run --name nginx-cache -p 80:80 -p 443:443 -v $PWD/nginx.conf:/etc/nginx/nginx.conf:ro nginx
