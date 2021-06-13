import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { GravarvideoPage } from './gravarvideo.page';

const routes: Routes = [
  {
    path: '',
    component: GravarvideoPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class GravarvideoPageRoutingModule {}
