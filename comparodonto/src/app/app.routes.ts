import { Routes } from '@angular/router';
import {ComparoDontoComponent} from './pages/comparo-donto/comparo-donto.component';
import {ByCategoriaComponent} from './pages/by-categoria/by-categoria.component';
import {ByMarcaComponent} from './pages/by-marca/by-marca.component';
import {HomeComponent} from './pages/home/home.component';
import {ProductComponent} from './pages/product/product.component';

export const routes: Routes = [
  {
    path: 'home',
    component: HomeComponent,
  },
  //Ruta para filtrar productos por nombre
  {
    path: 'comparador',
    component: ComparoDontoComponent,
  },
  {
    path: 'categoria',
    component: ByCategoriaComponent,
  },
  {
    path: 'marca',
    component: ByMarcaComponent,
  },
  {
    path: 'by/:id',
    component: ProductComponent,
  },
  // Ruta para cualquier página no encontrada
  { path: '**',
    redirectTo: 'home',
    pathMatch: 'full',
  }
];
