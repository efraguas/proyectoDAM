import { Component } from '@angular/core';
import {Product} from '../../interface/product';
import {ProductService} from '../../services/product.service';
import {CurrencyPipe} from '@angular/common';
import {SearchboxComponent} from '../../shared/searchbox/searchbox.component';

@Component({
  selector: 'app-by-categoria',
  standalone: true,
  imports: [
    CurrencyPipe,
    SearchboxComponent
  ],
  templateUrl: './by-categoria.component.html',
  styleUrl: './by-categoria.component.css'
})
export class ByCategoriaComponent {

  public products : Product [] = [];

  constructor(private producService : ProductService) {}

  //metodo para suscribirse al Observable y recuperar los resultados que emite

    getByCategoria(categoria: string | null):void {
    if(categoria)
    this.producService.filterCategoria(categoria)
      .subscribe(products=>{
        this.products = products;
      })
  }


}
