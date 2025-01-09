package com.comparodonto.odontoapi.odonto_api.exception;

import com.comparodonto.odontoapi.odonto_api.enums.HttpResponse;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class ProductException extends RuntimeException {
    private final HttpResponse response;

}

