import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { PujarvideoPage } from './pujarvideo.page';

const routes: Routes = [
  {
    path: '',
    component: PujarvideoPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class PujarvideoPageRoutingModule {}
