FROM node:alpine as build

COPY package.json package.json
RUN npm install
RUN apk --no-cache add curl

COPY . .
RUN npm run build

CMD npm start

FROM nginx:alpine

COPY --from=build /build /usr/share/nginx/html
COPY --from=build nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
