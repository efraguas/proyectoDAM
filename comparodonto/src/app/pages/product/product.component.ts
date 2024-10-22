import {Component, OnInit} from '@angular/core';
import {CurrencyPipe} from '@angular/common';
import {SearchboxComponent} from '../../shared/searchbox/searchbox.component';
import {ActivatedRoute, Router} from '@angular/router';
import {ProductService} from '../../services/product.service';
import {switchMap} from 'rxjs';
import {Product} from '../../interface/product';

@Component({
  selector: 'app-product',
  standalone: true,
  imports: [
    CurrencyPipe,
    SearchboxComponent
  ],
  templateUrl: './product.component.html',
  styleUrl: './product.component.css'
})
export class ProductComponent implements OnInit{
  public product? : Product;

  constructor(private activatedRoute: ActivatedRoute,
              private router : Router,
              private productService : ProductService) {
  }

  //
  ngOnInit(): void {
    this.activatedRoute.params
      .pipe(
        switchMap( ({id}) => this.productService.filter_by_id(id)),
        )
      .subscribe(product  =>{
        console.log(product);
        if(!product) {
          console.log('no hay producto');
          return
        }
        console.log(product)
        console.log(this.product);
        this.product = product;

      });

  }


}
