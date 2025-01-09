# Usa la imagen oficial de OpenJDK para ejecutar la app
FROM openjdk:17-jdk-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo JAR desde tu máquina local al contenedor
COPY target/odonto_api.jar /app/odonto_api.jar

# Expone el puerto 8080 donde Spring Boot escuchará
EXPOSE 8080

# Comando para ejecutar la aplicación Spring Boot
CMD ["java", "-jar", "odonto_api.jar"]
