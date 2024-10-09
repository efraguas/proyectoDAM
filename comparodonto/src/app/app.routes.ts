import { Routes } from '@angular/router';
import {ByNameComponent} from './pages/by-name/by-name.component';
import {ByCategoriaComponent} from './pages/by-categoria/by-categoria.component';
import {ByMarcaComponent} from './pages/by-marca/by-marca.component';
import {HomeComponent} from './pages/home/home.component';
import {ProductComponent} from './pages/product/product.component';

export const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
  },
  //Ruta para filtrar productos por nombre
  {
    path: 'byName',
    component: ByNameComponent,
    children: [
      {
        path: 'product',
        component: ProductComponent
      },
    ]
  },
  {
    path: 'byCategoria',
    component: ByCategoriaComponent,
  },
  {
    path: 'byMarca',
    component: ByMarcaComponent,
  },
  // Ruta para cualquier página no encontrada
  { path: '**',
    redirectTo: '',
    pathMatch: 'full',
  }
];
