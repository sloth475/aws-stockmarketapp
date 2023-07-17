import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-company-list',
  templateUrl: './company-list.component.html',
  styleUrls: ['./company-list.component.css']
})
export class CompanyListComponent {
  companies: any[] = [];
  newCompany: any = {};
  companyId: string;
  searchResult: any;
  showCompanyForm = false;
  stocks: any[] = [];

  constructor(private http: HttpClient) {
    // this.showCompanyForm = false;
  }
  toggleCompanyForm() {
    this.showCompanyForm = !this.showCompanyForm;
    this.newCompany = {}; // Reset the form fields when opening/closing the form
  }



  addCompany() {
    console.log("-----");
    console.log('Add Company:', this.newCompany);
    const payloads = {
      "ceo": this.newCompany.ceo,
      "turnover": this.newCompany.turnover,
      "companyId": this.newCompany.code,
      "stockexchange": this.newCompany.stockexchange,
      "name": this.newCompany.name

    };
    const payload = JSON.stringify(payloads);
    console.log("=====", payload);
    const url = 'https://hb6yiq7ovb.execute-api.ap-south-1.amazonaws.com/prod/company?company=101';
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'x-api-key': 'knSTS5pD5K85wbnruXEo52cZF8CuIHe0amru3qxS'
    });

    this.http.post<any>(url, payload, { headers: headers }).subscribe(
      (response) => {
        console.log('Company added successfully:', response);
        this.listCompanies();
        // this.toggleCompanyForm();
        this.newCompany = {};
        this.showCompanyForm = false;
      },
      (error) => {
        console.log('Error adding company:', error);
      }
    );
  }

  listCompanies() {
    console.log("list compnay....");
    const headers = new HttpHeaders({ 'Content-Type': 'application/json', 'x-api-key': 'knSTS5pD5K85wbnruXEo52cZF8CuIHe0amru3qxS' });
    const url = 'https://hb6yiq7ovb.execute-api.ap-south-1.amazonaws.com/prod/companys?company=101'
    this.http.get<any>(url, { headers: headers }).subscribe(
      (response) => {
        this.companies = response;
      },
      (error) => {
        console.log('Error getting  companies:', error);
      }
    );
  }

  // showCompanyForm = false;
  // toggleCompanyForm() {
  //   this.showCompanyForm = !this.showCompanyForm;
  // }

  // openCompanyForm() {
  //   this.showCompanyForm = true;
  // }

  // closeCompanyForm(submitted: boolean) {
  //   if (submitted) {
  //     console.log('Company added successfully@@@@SSSS!');
  //   }
  //   this.showCompanyForm = false;
  // }

  searchText: string = '';

  searchCompany() {
    console.log("sssss");
    if (!this.companyId) {
      return;
    }

    const url = `https://hb6yiq7ovb.execute-api.ap-south-1.amazonaws.com/prod/company?companyId=${this.companyId}`;
    console.log("search compnay....");
    const headers = new HttpHeaders({ 'Content-Type': 'application/json', 'x-api-key': 'knSTS5pD5K85wbnruXEo52cZF8CuIHe0amru3qxS' });

    this.http.get<any>(url, { headers: headers }).subscribe(
      (response) => {
        this.searchResult = response;
        // alert(JSON.stringify(this.searchResult)); // Print the company details
      },
      (error) => {
        console.log('Error searching company:', error);
        this.searchResult = null;
      }
    );
    const url2 = `https://hb6yiq7ovb.execute-api.ap-south-1.amazonaws.com/prod/stocks?companyId=${this.companyId}`;

    this.http.get<any>(url2, { headers: headers }).subscribe(
      (response) => {
        console.log('Stocks:', response);
        this.stocks = response;
      },
      (error) => {
        console.log('Error fetching stocks:', error);
        this.stocks = []; // Clear the stock array if an error occurs
      }
    );
  }

  // openCompanyForm() {
  //   console.log("open form ....");
  //   this.showCompanyForm = true;
  //   this.newCompany = {}; // Reset the form fields when opening the form
  // }
}