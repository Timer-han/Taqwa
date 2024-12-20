FROM node:alpine

WORKDIR /home/node/app

COPY package.json package-lock.json ./
RUN npm install

RUN apk --no-cache add curl

COPY . ./

EXPOSE 3000

CMD npm start