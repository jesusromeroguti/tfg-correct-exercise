import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { PujarvideoPageRoutingModule } from './pujarvideo-routing.module';

import { PujarvideoPage } from './pujarvideo.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    PujarvideoPageRoutingModule
  ],
  declarations: [PujarvideoPage]
})
export class PujarvideoPageModule {}
