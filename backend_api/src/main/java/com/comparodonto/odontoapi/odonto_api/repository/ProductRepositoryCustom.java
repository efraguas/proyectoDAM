package com.comparodonto.odontoapi.odonto_api.repository;
import com.comparodonto.odontoapi.odonto_api.Models.Productos;
import java.util.List;

public interface ProductRepositoryCustom {
    List<Productos> find_nombre_filtrado(String nombre);
    List<Productos> find_categoria_filtrado(String categoria);
    List<Productos> find_marca_filtrado(String marca);

}
