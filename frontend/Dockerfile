FROM node:lts-alpine

WORKDIR /frontend

COPY package*.json ./

RUN npm install && npm cache clean --force

COPY . .

CMD ["npm", "run", "dev"]