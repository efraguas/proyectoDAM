package com.comparodonto.odontoapi.odonto_api.service;

import com.comparodonto.odontoapi.odonto_api.Models.Productos;

import java.util.List;
import java.util.Optional;

public interface ProductService {

    Optional<Productos> get_producto_id(String id);
    List<String> get_productos();
    List<Productos> get_producto_nombre(String nombre);
    List<Productos> get_producto_categoria(String categoria);
    List<Productos> get_producto_marca(String marca);

}
