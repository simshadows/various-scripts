import {NgModule} from '@angular/core';

import {ContentQueryDemoComponent} from './content-query-demo.component';
import {BarbazParentComponent} from './barbaz-parent.component';
import {FoobarChildComponent} from './foobar-child.component';

@NgModule({
  declarations: [
    ContentQueryDemoComponent,
    BarbazParentComponent,
    FoobarChildComponent,
  ],
  imports: [],
  providers: [],
  bootstrap: [],
  exports: [ContentQueryDemoComponent],
})
export class ContentQueryDemoModule {}
