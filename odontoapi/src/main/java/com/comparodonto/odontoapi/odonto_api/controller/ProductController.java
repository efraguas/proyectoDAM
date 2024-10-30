package com.comparodonto.odontoapi.odonto_api.controller;


import com.comparodonto.odontoapi.odonto_api.Models.Productos;
import com.comparodonto.odontoapi.odonto_api.service.ProductService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin
@RestController
@RequestMapping("/api/odonto_api")
@RequiredArgsConstructor
public class ProductController {

    @Autowired
    private ProductService productService;


    //Endppoint obtener por id
    @GetMapping("/{id}")
    public ResponseEntity<Productos> get_by_id(@PathVariable String id){
        return productService.get_producto_id(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
    //Endpoint de obtener por nombre ordenado por precio
    @GetMapping("/nombre")
    public List<Productos>get_by_nombre(@RequestParam String nombre){
        return productService.get_producto_nombre(nombre);
    }

    //Endpoint de obtener por categoria ordenado por precio
    @GetMapping("/categoria")
    public List<Productos>get_by_categoria(@RequestParam String categoria){
        return productService.get_producto_categoria(categoria);
    }

    //Endpoint de obtener por marca ordenado por precio
    @GetMapping("/marca")
    public List<Productos>get_by_marca(@RequestParam String marca){
        return productService.get_producto_marca(marca);
    }

    //Endppoint para obtener todos los productos
    @GetMapping("/productos")
    public ResponseEntity<List<Productos>>get_productos(){
        List<Productos> productos = productService.get_productos();
        return ResponseEntity.ok(productos);
    }


}
