package com.comparodonto.odontoapi.odonto_api.exception;
import com.comparodonto.odontoapi.odonto_api.dto.ApiDTO;
import com.comparodonto.odontoapi.odonto_api.enums.HttpResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler({
            ProductException.class,
            ProductNotFoundException.class,
            InternalServerErrorException.class
    })
    public ResponseEntity<ApiDTO> handleProductException(RuntimeException ex) {
        HttpResponse response;

        switch (ex.getClass().getSimpleName()){
            case "ProductException":
                response = ((ProductException) ex).getResponse();
                break;
            case "ProductNotFoundException":
                response = ((ProductNotFoundException) ex).getResponse();
                break;
            default:
                response = HttpResponse.INTERNAL_SERVER_ERROR;
                break;
        }
        return ResponseEntity
                .status(response.getStatus())
                .body(new ApiDTO(response.getStatus(), response.getMensaje()));
    }
}
