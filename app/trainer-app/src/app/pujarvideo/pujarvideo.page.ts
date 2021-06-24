import { Component, OnInit } from '@angular/core';

import { HttpClient } from '@angular/common/http';

// import { FileTransfer, FileUploadOptions, FileTransferObject } from '@ionic-native/file-transfer/ngx';
import { File } from '@ionic-native/file';

import { AlertComponentComponent} from  '../components/alert-component/alert-component.component';
import { LoadingControllerComponent } from '../components/loading-controller/loading-controller.component';

@Component({
  selector: 'app-pujarvideo',
  templateUrl: './pujarvideo.page.html',
  styleUrls: ['./pujarvideo.page.scss'],
  providers: [AlertComponentComponent, LoadingControllerComponent]
})
export class PujarvideoPage implements OnInit {

  constructor(private http: HttpClient, private alertComponent: AlertComponentComponent, private loadingController: LoadingControllerComponent) { }

  file: File = null;
  baseApiUrl = 'http://127.0.0.1:3000/predict';
  res = [];
  text = 'Penja un vídeo per a obtenir un resultat. Pots tornar a veure els requeriments més avall.';
  htmlToAdd = '';
  comptador = 0;
  

  upload(){

    if(this.file == null){
      this.alertComponent.presentAlert('No hi ha cap fitxer seleccionat. Selecciona un abans de clicar "Puja".');
    } else {
      // this.loadingController.presentLoading();
      // Create form data
      const formData = new FormData();     
      
      this.res = []
      // this.text = ''
      // Store form name as "file" with file data
      formData.append("videofile", this.file, this.file.name);
      console.log(formData.getAll);

      // Make http post request over api
      // with formData as req
      return this.http.post(this.baseApiUrl, formData)
      .subscribe(data => {
        console.log(data);
        this.res = data["Resultat"]
        console.log(this.res);
        this.tractarCodi();
      }, (err) => {
        this.tractarErrorConnexio();
        console.log(err);
      });
    }


  }

  tractarErrorConnexio(){
    this.text="Sembla ser que hi ha algun problema de connexió.";
    document.getElementById("resposta").innerHTML = this.text;
  }

  tractarCodi() {    
    if(this.res.includes("good")) {
      this.loadingController.presentLoading();
      
      if(this.res.length == 1){
        this.text = 'La teva esquat és correcte. Continua així!';
      }
      else {
        this.text = 'Creiem que tens un petit error, però per a estar segurs grava un altre vídeo. ';
        if(this.res.includes("no90")) {
          this.text += 'Pot ser que no baixis suficientment. Flexiona més els genolls fins a arribar com a mínim a un angle de 90 graus entre la cuixa i el bessó. ';
        }
        if(this.res.includes("pesEndavant")) {
          this.text += "Pot ser que tiris el pes endavant. Assegura't de no aixecar els talons i tirar el cul enrere. ";
        }
        if(this.res.includes("torsoInclinat")) {
          this.text += "Pot ser que inclinis massa el tors. A l'hora de fer l'esquat, el tors es queda fix i baixa a la mateixa vegada que la resta del cos. ";
        }
        if(this.res.includes("desnivellPeus")) {
          this.text += "Pot ser que tinguis els peus mal posats. Prova de posar-los en paral·lel i a la mateixa alçada. ";
        }
        if(this.res.includes("pesEndavant") && this.res.length == 2){
          this.text = "Sembla que el teu esquat és correcte, però per a estar segurs grava un altre vídeo.";
          this.comptador += 1;
          if(this.comptador == 3){
            this.text = "Pot ser que tiris el pes endavant. Assegura't de no aixecar els talons i tirar el cul enrere.";
            this.comptador = 0;
          }
        }
      }     
    }
    else if(this.res.includes("bad")) {
      this.loadingController.presentLoading();
      
      if(this.res.length == 1) {
        this.text = "Sembla que estas fent bé l'exercici, però pot haver-hi un error en la manera en que l'has gravat. Si vols estar segur, torna'l a fer de nou.";
        this.comptador += 1;
        if(this.comptador == 3){
          this.text = "Sembla que estas fent bé l'exercici, però pot haver-hi un error en la manera en que l'has gravat.";
          this.comptador = 0;
        }
      }
      else {
        this.loadingController.presentLoading();
        
        this.text = '';
        if(this.res.includes("no90")) {
          this.text += 'No baixes suficientment. Flexiona més els genolls fins a arribar com a mínim a un angle de 90 graus entre la cuixa i el bessó. ';
        }
        if(this.res.includes("pesEndavant")) {
          this.text += "Tires el pes endavant. Assegura't de no aixecar els talons i tirar el cul enrere. ";
        }
        if(this.res.includes("torsoInclinat")) {
          this.text += "Inclines massa el tors. A l'hora de fer l'esquat, el tors es queda fix i baixa a la mateixa vegada que la resta del cos. ";
        }
        if(this.res.includes("desnivellPeus")) {
          this.text += "Tens els peus mal posats. Prova de posar-los en paral·lel i a la mateixa alçada. ";
        }
      }
    }
    else if(this.res.includes("noVideo")) {
      this.alertComponent.presentAlert("Només s'accepten arxius de vídeo. Si us plau puja un vídeo!");
    }
    else if(this.res.includes("errorDuracio")) {
      this.alertComponent.presentAlert("Has pujat un vídeo massa llarg. Si us plau penja'n un que s'adapti als requeriments.");
    }
    
    document.getElementById("resposta").innerHTML = this.text;
    // this.htmlToAdd = '<ion-col class="res-col"><ion-card><ion-card-title>Resultat</ion-card-title><ion-card-content><div id="resposta"></div></ion-card-content></ion-card></ion-col><ion-col><ion-card class="video-card"><ion-card-title>Vídeo</ion-card-title><ion-card-content><ion-img class="video" src="assets/costat_fondo.png"></ion-img></ion-card-content></ion-card></ion-col>';

  }

  ngOnInit() {
  }

  onChange(event) {
    this.file = event.target.files[0];
    // console.log(this.file.name)
    // this.file.checkDir(this.file.dataDirectory, 'mydir').then(_ => console.log('Directory exists')).catch(err =>console.log("Directory doesn't exist"));
  }

}

