package com.comparodonto.odontoapi.odonto_api.repository;

import com.comparodonto.odontoapi.odonto_api.Models.Productos;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;

import java.util.List;


@Repository
public class ProductRepositoryImpl implements ProductRepositoryCustom {

    @Autowired
    private MongoTemplate mongoTemplate;
    @Override
    public List<Productos> find_nombre_filtrado(String nombre){
        Query query = new Query();
        query.addCriteria(Criteria.where("nombre").regex(nombre, "i"));
        query.with(Sort.by(Sort.Direction.ASC, "precio"));
        return mongoTemplate.find(query, Productos.class);
    }
    @Override
    public List<Productos> find_categoria_filtrado(String categoria){
        Query query = new Query();
        query.addCriteria(Criteria.where("categoria").regex(categoria, "i"));
        query.with(Sort.by(Sort.Direction.ASC, "precio"));
        return mongoTemplate.find(query, Productos.class);
    }
    @Override
    public List<Productos> find_marca_filtrado(String marca){
        Query query = new Query();
        query.addCriteria(Criteria.where("marca").regex(marca, "i"));
        query.with(Sort.by(Sort.Direction.ASC, "precio"));
        return mongoTemplate.find(query, Productos.class);
    }


}