# pull official base image
FROM node:13.12.0-alpine

# set working directory
WORKDIR /frontend_app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json package-lock.json ./
COPY src/ ./src/
COPY public/ ./public/

RUN npm install

# start app
CMD ["npm", "start"]
