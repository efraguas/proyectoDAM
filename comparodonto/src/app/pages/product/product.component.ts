import { Component } from '@angular/core';
import {CurrencyPipe} from '@angular/common';
import {SearchboxComponent} from '../../shared/searchbox/searchbox.component';
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
export class ProductComponent {
  public products : Product [] = [];
}
