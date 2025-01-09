import { Routes } from '@angular/router';
import {ComparoDontoComponent} from './pages/comparo-donto/comparo-donto.component';
import {HomeComponent} from './pages/home/home.component';
import {ProductComponent} from './pages/product/product.component';
import {ContactComponent} from './pages/contact/contact.component';

export const routes: Routes = [
  {
    path: 'home',
    component: HomeComponent,
  },
  {
    path: 'comparador',
    component: ComparoDontoComponent,
  },
  {
    path: 'contacto',
    component: ContactComponent,
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
