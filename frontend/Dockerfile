FROM node:13.12.0-alpine

WORKDIR /frontend_app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json package-lock.json ./
COPY src/ ./src/
COPY public/ ./public/

RUN npm install

CMD ["npm", "start"]
