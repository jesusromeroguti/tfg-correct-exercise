import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { IniciPageRoutingModule } from './inici-routing.module';

import { IniciPage } from './inici.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    IniciPageRoutingModule
  ],
  declarations: [IniciPage]
})
export class IniciPageModule {}
