import {
  Component,
  ContentChild,
} from '@angular/core';

import {FoobarChildComponent} from './foobar-child.component';

@Component({
  selector: 'barbaz-parent',
  template: `
    <div>
      <p>content query demo barbaz</p>
      <ng-content/>
    </div>
  `,
  standalone: false,
})
export class BarbazParentComponent {
  @ContentChild(FoobarChildComponent)
  foobarChild!: FoobarChildComponent;

  ngAfterContentInit() {
    console.log(this.foobarChild);
  }
}
