package com.comparodonto.odontoapi.odonto_api.dto;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.http.HttpStatus;

@Data
@AllArgsConstructor
public class ApiDTO {

    //DTO informacion de los estados de las peticiones
    private HttpStatus status;
    private String mensaje;



}
