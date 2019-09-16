import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class HttpService {
  constructor(private _http: HttpClient) { 
  }
  getTasks(){
    console.log("In the Service!");
    console.log("Going to Express Routes!");
    return this._http.get('/tasks');
  }
  getTask(id){
    return this._http.get(`/tasks/${id}`);
  }
  
}
