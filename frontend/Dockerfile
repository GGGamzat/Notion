FROM node:24-alpine3.21

WORKDIR /app

COPY package*.json ./

# Установите все зависимости (не только production)
RUN npm install

COPY . .

EXPOSE 3000

# Для разработки используем npm start
CMD ["npm", "start"]