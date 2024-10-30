package com.comparodonto.odontoapi.odonto_api.Models;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.MongoId;


@Document(collection = "Productos") // coleccion de MongoDB que vamos a mapear
@Data // Genera getters, setters, toString, equals, hashCode
@NoArgsConstructor  // Genera un constructor sin argumentos
@AllArgsConstructor // Genera un constructor con todos los argumentos
public class Productos {
    @Id
    private String id;
    private String nombre;
    private String marca;
    private String categoria;
    private String subcategoria;
    private String imagen;
    private String url;
    private Double precio;



}
