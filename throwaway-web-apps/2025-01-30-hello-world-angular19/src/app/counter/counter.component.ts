import {Component, Input} from '@angular/core';
import {FormGroup, FormBuilder} from '@angular/forms';

@Component({
  selector: 'hello-counter',
  templateUrl: './counter.component.html',
  styleUrl: './counter.component.scss',
  standalone: false,
})
export class CounterComponent {
  @Input() labelName!: string;

  foobarIncClick() {
    console.log('lmao ayy');
    this.foobarForm.patchValue({
      cntValue: Number(this.foobarForm.value.cntValue) + 1,
      //cntValue: 9,
      myStr: (this.foobarForm.value.cntValue % 2) ? 'lmao' : 'ayy',
    });
  }

  foobarForm: FormGroup;

  constructor(fb: FormBuilder) {
    this.foobarForm = fb.group({
      cntValue: 7,
      myStr: 'ayy',
    });
  }
}
