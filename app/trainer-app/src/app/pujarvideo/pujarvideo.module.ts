import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { PujarvideoPageRoutingModule } from './pujarvideo-routing.module';

import { PujarvideoPage } from './pujarvideo.page';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    PujarvideoPageRoutingModule,
    NgbModule
  ],
  declarations: [PujarvideoPage]
})
export class PujarvideoPageModule {}
