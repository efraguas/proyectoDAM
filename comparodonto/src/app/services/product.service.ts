import { Injectable } from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {catchError, map, Observable, of} from 'rxjs';
import {Product} from '../interface/product';

@Injectable({
  providedIn: 'root'
})
export class ProductService {

  //url de la api
  private apiUrl : string = "http://localhost:8080/api/odonto_api";
  constructor(private http: HttpClient) { }


  //Metodo para acceder al endpoint de la api filtrado por nombre
  filterName(nombre: string): Observable<Product[]> {
    const params : HttpParams = new HttpParams().set("nombre", nombre);
    return this.http.get<Product []>(`${this.apiUrl}/nombre`,{params})
      .pipe(
        catchError( () => of([]))
      );

  }

  //Metodo para acceder al endpoint de la api filtrado por marca
  filterMarca (marca : string): Observable<Product []> {
    const params : HttpParams = new HttpParams().set("marca", marca);
    return this.http.get<Product []>(`${this.apiUrl}/marca`,{params})
      .pipe(
        catchError( () => of([]))
      );
  }

  //Metodo para acceder al endpoint de la api filtrados por categoria
  filterCategoria (categoria : string): Observable<Product []> {
    const params : HttpParams = new HttpParams().set("categoria", categoria);
    return this.http.get<Product []>(`${this.apiUrl}/categoria`,{params})
      .pipe(
        catchError( () => of([]))
      );
  }

  filter_by_id(id : string): Observable<Product | null> {
    //const params : HttpParams = new HttpParams().set("id", id);
    return this.http.get<Product >(`${this.apiUrl}/${id}`)
      .pipe(
        map(product => product ? product : null),
        catchError( () => of(null))
      );
  }





}
