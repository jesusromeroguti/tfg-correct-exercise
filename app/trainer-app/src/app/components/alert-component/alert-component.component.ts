import { Component, OnInit } from '@angular/core';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-alert-component',
  templateUrl: './alert-component.component.html',
  styleUrls: ['./alert-component.component.scss'],
})
export class AlertComponentComponent  {

  constructor(public alertController: AlertController) { }

  async presentAlert(message) {
    const alert = await this.alertController.create({
      cssClass: 'alert-component.component.scss',
      header: 'Alerta',
      message: message,
      buttons: ["D'acord"]
    });

    await alert.present();

    const { role } = await alert.onDidDismiss();
    console.log('onDidDismiss resolved with role', role);
  }

  

}
