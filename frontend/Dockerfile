FROM node:21.7.1-alpine3.19

WORKDIR /usr/src/app

COPY package*.json ./
COPY index* ./

RUN npm install

EXPOSE 3000

CMD ["node", "index.js"]