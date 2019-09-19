import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class HttpService {
  constructor(private _http: HttpClient) { }
  getSharks(){
    return this._http.get('/api/sharks');
  }
  getShark(id){
    return this._http.get(`/api/sharks/${id}`);
  }
  createShark(shark){
    return this._http.post('/api/sharks', shark);
  }
  updateShark(id,shark){
    return this._http.put(`/api/sharks/${id}`, shark);
  }
  deleteShark(id){
    return this._http.delete(`/api/sharks/${id}`);
  }
}
