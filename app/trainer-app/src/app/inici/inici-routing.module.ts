import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { IniciPage } from './inici.page';

const routes: Routes = [
  {
    path: '',
    component: IniciPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class IniciPageRoutingModule {}
