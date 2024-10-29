package com.comparodonto.odontoapi.odonto_api.repository;

import com.comparodonto.odontoapi.odonto_api.Models.Productos;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface ProductRepository extends MongoRepository<String, Productos>, ProductRepositoryCustom {
}
