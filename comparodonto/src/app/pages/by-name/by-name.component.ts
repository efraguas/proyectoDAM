import { Component } from '@angular/core';
import {Product} from '../../interface/product';
import {ProductService} from '../../services/product.service';
import {SearchboxComponent} from '../../shared/searchbox/searchbox.component';
import {CurrencyPipe} from '@angular/common';

@Component({
  selector: 'app-by-name',
  standalone: true,
  imports: [
    SearchboxComponent,
    CurrencyPipe
  ],
  templateUrl: './by-name.component.html',
  styleUrl: './by-name.component.css'
})
export class ByNameComponent {


  public products : Product [] = [];

  constructor(private producService : ProductService) {}

  //metodo para suscribirse al Observable y recuperar los resultados que emite

  getByName(name: string):void {
    this.producService.filterName(name)
      .subscribe(products =>{
        console.log("Datos: ", products)
        this.products = products;
      })
  }

}
