package com.comparodonto.odontoapi.odonto_api.service;
import com.comparodonto.odontoapi.odonto_api.Models.Productos;
import com.comparodonto.odontoapi.odonto_api.exception.ProductNotFoundException;
import com.comparodonto.odontoapi.odonto_api.repository.ProductRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.net.http.HttpResponse;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class ProductServiceImpl implements ProductService{

    @Autowired
    private ProductRepository productRepository;

    @Override
    public Optional<Productos> get_producto_id(String id) {
        return productRepository.findById(id);
    }

    @Override
    public List<Productos> get_productos() {
        return productRepository.findAll();
    }

    @Override
    public List<Productos> get_producto_nombre(String nombre) {
        return productRepository.find_nombre_filtrado(nombre);
    }

    @Override
    public List<Productos> get_producto_categoria(String categoria) {
        return productRepository.find_categoria_filtrado(categoria);
    }

    @Override
    public List<Productos> get_producto_marca(String marca) {
        return productRepository.find_marca_filtrado(marca);
    }
}
