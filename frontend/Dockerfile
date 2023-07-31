FROM node:13.12.0-alpine

WORKDIR /frontend_app

ENV PATH /app/node_modules/.bin:$PATH

COPY . .

RUN npm install

CMD ["npm", "start"]
