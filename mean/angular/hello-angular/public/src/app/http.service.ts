import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class HttpService {
  constructor(private _http: HttpClient) { 
    this.getTasks();
    this.getTask("5d28b45fb2c2a74560e7d8d9");
    this.createTask({title: "Something cool", description: "something equally cool", isCompleted: false});
    this.updateTask("5d28b45fb2c2a74560e7d8d9", {title: "Something cool", description: "something equally cool", isCompleted: false});
    this.deleteTask("5d28b45fb2c2a74560e7d8d9");
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
