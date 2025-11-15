import {NgModule} from '@angular/core';

import {DepsDemoAAComponent} from './deps-demo-a-a.component';
import {DepsDemoABComponent} from './deps-demo-a-b.component';

@NgModule({
  declarations: [
    DepsDemoAAComponent,
    DepsDemoABComponent,
  ],
  imports: [],
  providers: [],
  bootstrap: [],
  exports: [DepsDemoAAComponent],
})
export class DepsDemoAModule {}
