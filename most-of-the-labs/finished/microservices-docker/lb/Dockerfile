FROM nginx:alpine
ARG USERS_SVC_HOST=users-service:3000
ARG PRODUCTS_SVC_HOST=products-service:3000
COPY nginx.conf.template /etc/nginx/nginx.conf.template
RUN envsubst '${USERS_SVC_HOST} ${PRODUCTS_SVC_HOST}' \
      < /etc/nginx/nginx.conf.template \
      > /etc/nginx/nginx.conf \
    && rm /etc/nginx/nginx.conf.template
EXPOSE 80
