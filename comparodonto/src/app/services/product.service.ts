import { Injectable } from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Product} from '../interface/product';

@Injectable({
  providedIn: 'root'
})
export class ProductService {

  //url de la api
  private apiUrl : string = "http://127.0.0.1:5000/productos"
  constructor(private http: HttpClient) { }


  //Metodo para acceder al endpoint de la api filtrado por nombre
  filterName (nombre : string): Observable<Product []> {
    const params : HttpParams = new HttpParams().set("nombre", nombre)
    return this.http.get<Product []>(`${this.apiUrl}/nombre`,{params})
  }

  //Metodo para acceder al endpoint de la api filtrado por marca
  filterMarca (marca : string): Observable<Product []> {
    const params : HttpParams = new HttpParams().set("marca", marca)
    return this.http.get<Product []>(`${this.apiUrl}/marca`,{params})
  }

  //Metodo para acceder al endpoint de la api filtrados por categoria
  filterCategoria (categoria : string): Observable<Product []> {
    const params : HttpParams = new HttpParams().set("categoria", categoria)
    return this.http.get<Product []>(`${this.apiUrl}/categoria`,{params})
  }





}
