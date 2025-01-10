Para levantar los contenedores es necesario:
Doker Compose:
1. disponer de docker desktop instalado
2.Docker y Docker Compose instalado
3. Ejecutar los siguiente:
    -En Springboot
        ejecuta mvn clean
                mvn install
    -En Angular 
        ejecuta npm build --configuration production
4. Ejecutar los siguientes comandos en la raiz del proyecto
        docker-compose build
        doker-compose up -d

