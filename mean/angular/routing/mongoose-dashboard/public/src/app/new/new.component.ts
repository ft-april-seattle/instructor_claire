import { HttpService } from './../http.service';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-new',
  templateUrl: './new.component.html',
  styleUrls: ['./new.component.css']
})
export class NewComponent implements OnInit {
  constructor(private _httpService: HttpService, private _router: Router) { }
  newShark: any;

  ngOnInit() {
    this.newShark = {name: "", species: "", location: "", img: ""};
  }

  onSubmit(){
    this._httpService.createShark(this.newShark).subscribe(data => {
      console.log(data);
      this.newShark = {name: "", species: "", location: "", img: ""};
      this._router.navigate(['/sharks']);
    });
  }

}
