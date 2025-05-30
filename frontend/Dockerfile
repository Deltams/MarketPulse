FROM node:lts-alpine

WORKDIR /frontend

COPY package*.json ./

RUN npm install && npm cache clean --force

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]