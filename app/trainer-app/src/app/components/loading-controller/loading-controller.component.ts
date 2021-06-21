import { Component, OnInit } from '@angular/core';
import { LoadingController } from '@ionic/angular';

@Component({
  selector: 'app-loading-controller',
  templateUrl: './loading-controller.component.html',
  styleUrls: ['./loading-controller.component.scss'],
})
export class LoadingControllerComponent  {

  constructor(public loadingController: LoadingController) { }

  async presentLoading() {
    const loading = await this.loadingController.create({
      cssClass: 'loading-controler.component.scss',
      message: 'Carregant resposta...',
      duration: 1000
    });
    await loading.present();

    const { role, data } = await loading.onDidDismiss();
    console.log('Loading dismissed!');
  }

  async destroy(){
    this.loadingController.dismiss();
  }



}
