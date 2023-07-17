import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-company-form',
  templateUrl: './company-form.component.html',
  styleUrls: ['./company-form.component.css']
})
export class CompanyFormComponent {
  company: any = {};

  @Output() close = new EventEmitter<boolean>();

  submitForm() {
    // Perform form submission logic, e.g., send the data to a server
    // You can access the entered company details using this.company object

    // Emit the close event and pass 'true' to indicate successful form submission
    this.close.emit(true);
  }

  closeForm() {
    // Emit the close event and pass 'false' to indicate form cancellation
    this.close.emit(false);
  }
}
