import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { GravarvideoPageRoutingModule } from './gravarvideo-routing.module';

import { GravarvideoPage } from './gravarvideo.page';


@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    GravarvideoPageRoutingModule
  ],
  declarations: [GravarvideoPage]
})
export class GravarvideoPageModule {}
