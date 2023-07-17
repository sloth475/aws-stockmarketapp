import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { CompanyListComponent } from './company-list/company-list.component';
import { CompanyFormComponent } from './company-form/company-form.component';

const routes: Routes = [
  { path: 'company-list', component: CompanyListComponent },
  { path: '', redirectTo: '/company-list', pathMatch: 'full' },
];

@NgModule({
  declarations: [AppComponent, CompanyListComponent, CompanyFormComponent],
  imports: [BrowserModule, FormsModule, RouterModule.forRoot(routes), HttpClientModule],
  providers: [],
  bootstrap: [AppComponent],

})
export class AppModule { }
