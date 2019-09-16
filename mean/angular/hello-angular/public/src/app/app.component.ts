import { HttpService } from './http.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(private _httpService: HttpService){}
  title = 'public';
  allTasks: any;
  isClicked = false;
  oneTask: any;
  

  ngOnInit(){
    this.getTasksFromService();
  }

  getTasksFromService(){
    console.log("In Angular Component.");
    console.log("Going to Service!");
    this._httpService.getTasks().subscribe(data => {
      console.log("Retrieved data! Back in Angular");
      // console.log(data);
      this.allTasks = data;
      console.log(this.allTasks);
    })
  }
  showTask(){
    this.oneTask = this.allTasks[0];
    this.isClicked = true;
  }
}
