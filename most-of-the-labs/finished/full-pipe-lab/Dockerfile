FROM node:22-alpine

WORKDIR /app

COPY ./package-lock.json /app/

COPY ./package.json /app/

RUN npm ci

COPY . .

EXPOSE 3000

CMD ["node", "app.js"]



