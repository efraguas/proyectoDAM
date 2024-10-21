import { Component } from '@angular/core';
import {Product} from '../../interface/product';
import {ProductService} from '../../services/product.service';
import {CurrencyPipe} from '@angular/common';
import {SearchboxComponent} from '../../shared/searchbox/searchbox.component';

@Component({
  selector: 'app-by-marca',
  standalone: true,
  imports: [
    CurrencyPipe,
    SearchboxComponent
  ],
  templateUrl: './by-marca.component.html',
  styleUrl: './by-marca.component.css'
})
export class ByMarcaComponent {
  public products : Product [] = [];

  constructor(private producService : ProductService) {}

  //metodo para suscribirse al Observable y recuperar los resultados que emite

  getByMarca(marca: string | null):void {
    if(marca)
    this.producService.filterMarca(marca)
      .subscribe(products =>{
        this.products = products;
      })
  }

}
