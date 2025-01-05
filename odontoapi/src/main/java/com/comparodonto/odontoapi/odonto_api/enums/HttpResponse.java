package com.comparodonto.odontoapi.odonto_api.enums;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;

@Getter
@RequiredArgsConstructor
public enum HttpResponse {

    //Mensaje de respuesta
    SUCCESS(HttpStatus.OK, "Operacion ejecutada con exito"),
    PRODUCT_NOT_FOUND(HttpStatus.NOT_FOUND, "Error: Producto no encontrado"),
    INVALID_INPUT(HttpStatus.BAD_REQUEST, "Error: Parametros de entrada invalidos"),
    INTERNAL_SERVER_ERROR(HttpStatus.INTERNAL_SERVER_ERROR, "Error: interno del servidor");


    private final HttpStatus status;
    private final String mensaje;

}
