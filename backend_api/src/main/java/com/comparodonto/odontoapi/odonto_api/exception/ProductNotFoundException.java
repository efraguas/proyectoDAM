package com.comparodonto.odontoapi.odonto_api.exception;

import com.comparodonto.odontoapi.odonto_api.enums.HttpResponse;

public class ProductNotFoundException extends ProductException {

    public ProductNotFoundException() {
        super(HttpResponse.PRODUCT_NOT_FOUND);
    }
}


