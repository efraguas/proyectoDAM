package com.comparodonto.odontoapi.odonto_api.exception;

import com.comparodonto.odontoapi.odonto_api.enums.HttpResponse;

public class InternalServerErrorException extends ProductException {
    public InternalServerErrorException() {
        super(HttpResponse.INTERNAL_SERVER_ERROR);
    }
}

