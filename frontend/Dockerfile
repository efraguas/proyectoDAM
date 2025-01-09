# Usa una imagen base de Node.js para construir la app
FROM node:18 AS build

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de configuración del proyecto
COPY package.json package-lock.json ./

# Instala las dependencias de Angular
RUN npm install

# Copia el resto de los archivos del proyecto
COPY . .

# Construye la aplicación Angular para producción
RUN npm run build --prod

# Usa Nginx para servir la app Angular
FROM nginx:alpine

# Copia los archivos generados por Angular en la carpeta de Nginx
COPY --from=build /app/dist/comparodonto /usr/share/nginx/html

# Expone el puerto 80
EXPOSE 80

# Comando para iniciar Nginx
CMD ["nginx", "-g", "daemon off;"]
