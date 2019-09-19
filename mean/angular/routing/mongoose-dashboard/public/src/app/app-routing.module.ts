import { AppComponent } from './app.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ShowAllComponent } from './show-all/show-all.component';
import { ShowOneComponent } from './show-one/show-one.component';
import { NewComponent } from './new/new.component';

const routes: Routes = [
  { path: 'sharks', component: ShowAllComponent },
  { path: 'sharks/new', component: NewComponent },
  { path: 'sharks/:id', component: ShowOneComponent },
  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
