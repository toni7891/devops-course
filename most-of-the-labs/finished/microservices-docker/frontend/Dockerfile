FROM nginx:alpine
ARG LB_HOST=lb
COPY nginx.conf /etc/nginx/nginx.conf.template
RUN envsubst '${LB_HOST}' \
      < /etc/nginx/nginx.conf.template \
      > /etc/nginx/nginx.conf \
    && rm /etc/nginx/nginx.conf.template
COPY public/ /usr/share/nginx/html/
EXPOSE 80