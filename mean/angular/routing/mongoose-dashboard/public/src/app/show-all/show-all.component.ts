import { HttpService } from './../http.service';
import { Component, OnInit } from '@angular/core';
@Component({
  selector: 'app-show-all',
  templateUrl: './show-all.component.html',
  styleUrls: ['./show-all.component.css']
})
export class ShowAllComponent implements OnInit {
  constructor(private _httpService: HttpService) { }
  sharks: any;
  selectedShark: any;

  ngOnInit() {
    this.getSharksFromService();
  }
  getSharksFromService(){
    this._httpService.getSharks().subscribe(data => {
      console.log(data);
      this.sharks = data;
    })
  }
  sharkToShow(shark){
    this.selectedShark = shark;
  }
}
