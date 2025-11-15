import {NgModule} from '@angular/core';
import {ReactiveFormsModule} from '@angular/forms';

import {CounterComponent} from './counter.component';

@NgModule({
  declarations: [CounterComponent],
  imports: [ReactiveFormsModule],
  providers: [],
  bootstrap: [],
  exports: [CounterComponent],
})
export class CounterModule {}
