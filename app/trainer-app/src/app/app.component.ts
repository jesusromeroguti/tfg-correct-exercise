import { Component } from '@angular/core';
import { Platform } from '@ionic/angular';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss'],
})
export class AppComponent {
  navigate: any;
  constructor() {
      this.sideMenu();
    }


    sideMenu() {
      this.navigate =
      [
        {
          title : "Inici",
          url   : "/inici",
          icon  : "home"
        },
        {
          title : "Puja un vídeo",
          url   : "/pujarvideo",
          icon  : "cloud-upload-outline"
        },
        {
          title : "Grava un vídeo",
          url   : "/gravarvideo",
          icon  : "videocam-outline"
        },
        {
          title : "Informació",
          url   : "/info",
          icon  : "information-circle-outline"
        },
      ]
    }
}
