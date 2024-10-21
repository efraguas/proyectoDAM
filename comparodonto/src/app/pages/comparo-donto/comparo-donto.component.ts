import {Component} from '@angular/core';
import {Product} from '../../interface/product';
import {ProductService} from '../../services/product.service';
import {SearchboxComponent} from '../../shared/searchbox/searchbox.component';
import {CurrencyPipe} from '@angular/common';
import {ActivatedRoute, Router, RouterLink, RouterOutlet} from '@angular/router';
import {SelectBoxComponent} from '../../shared/select-box/select-box.component';
import {FormControl, ReactiveFormsModule} from '@angular/forms';
import Swal from 'sweetalert2';
import {BotonComponent} from '../../shared/boton/boton.component';

@Component({
  selector: 'app-by-name',
  standalone: true,
  imports: [
    SearchboxComponent,
    CurrencyPipe,
    RouterOutlet,
    RouterLink,
    SelectBoxComponent,
    BotonComponent,
    ReactiveFormsModule
  ],
  templateUrl: './comparo-donto.component.html',
  styleUrl: './comparo-donto.component.css'
})
export class ComparoDontoComponent {

  //propiedades
  public products: Product [] = [];
  public criterio : string | null = null;
  public selector: FormControl<string| null> = new FormControl<string | null>(null);

  constructor(private router: Router,
              private productService: ProductService,
              private route: ActivatedRoute) {
  }

  //metodo para gestionar el cambio del selector
  onSelectionChanged(seleccion: string | null): void {
    if (seleccion != null) {
      this.selector.setValue(seleccion);
    }
  }


  //Metodo para buscar productos y validar
  onSearch(busqueda: string): void {
    this.criterio = this.selector.value;
    if (!busqueda) {
      this.showError('El valor no puede estar vacio');
      return;
    }
    this.llamadaApi(this.criterio, busqueda);
  }

  //Metodo para aplicar el criterio de busqueda
  llamadaApi(seleccion: string | null, valor: string): void {
      switch (seleccion) {
        case 'nombre':
          this.productService.filterName(valor).subscribe({
            next: (products) => {
              console.log('Datos: ', products);
              this.products = products;
            },
            error: ():void => {
              this.showError('Error al buscar por nombre');
            },
          });
          break;
        case 'categoria':
          this.productService.filterCategoria(valor).subscribe({
            next: (products) => {
              console.log('Datos: ', products);
              this.products = products;
            },
            error: (): void => {
              this.showError('Error al buscar por nombre');
            },
          });
          break;
        case 'marca':
          this.productService.filterMarca(valor).subscribe({
            next: (products) => {
              console.log('Datos: ', products);
              this.products = products;
            },
            error: (): void  => {
              this.showError('Error al buscar por nombre');
            },
          });
          break;
      }


  }

  detalle(id: string): void {
    // Navegar a la página del producto usando el ID
    console.log("ID:", id)
    this.router.navigate([`byName/${id}`]);
  }

  showError(mensaje: string): void {
    Swal.fire({
      title: "Error!",
      text: mensaje,
      icon: "error"
    });
  }


}
