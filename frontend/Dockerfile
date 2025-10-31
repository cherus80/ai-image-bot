# Frontend Dockerfile (Production) для AI Image Generator Bot

# Stage 1: Build
FROM node:20-alpine AS build

WORKDIR /app

# Копирование package.json и package-lock.json
COPY package*.json ./

# Установка зависимостей
RUN npm ci --only=production

# Копирование кода
COPY . .

# Build приложения
RUN npm run build

# Stage 2: Production
FROM nginx:alpine

# Копирование build файлов
COPY --from=build /app/dist /usr/share/nginx/html

# Копирование nginx конфигурации
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose порт
EXPOSE 80

# Запуск nginx
CMD ["nginx", "-g", "daemon off;"]
