FROM nginx:alpine

RUN rm -rf /usr/share/nginx/html/*

COPY homer.jpg /usr/share/nginx/html/
COPY index.html /usr/share/nginx/html/
COPY script.js /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/

CMD ["nginx", "-g", "daemon off;"]
