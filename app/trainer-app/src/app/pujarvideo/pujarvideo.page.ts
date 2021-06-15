import { Component, OnInit } from '@angular/core';

import { HttpClient } from '@angular/common/http';

// import { FileTransfer, FileUploadOptions, FileTransferObject } from '@ionic-native/file-transfer/ngx';
import { File } from '@ionic-native/file';

@Component({
  selector: 'app-pujarvideo',
  templateUrl: './pujarvideo.page.html',
  styleUrls: ['./pujarvideo.page.scss'],
})
export class PujarvideoPage implements OnInit {

  constructor(private http: HttpClient) { }

  file: File = null;
  baseApiUrl = 'http://127.0.0.1:3000/predict'
  res = []
  text = ''
  
  upload(){

    // Create form data
    const formData = new FormData();     
    
    this.res = []
    this.text = ''
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
      console.log(err);
    });

  }

  tractarCodi() {    
    if(this.res.includes("good")) {
      if(this.res.length == 1){
        this.text = 'Ets el puto amo';
      }
      else {
        this.text = 'Creiem que tens un petit error, però per a estar segurs grava un altre vídeo. ';
        if(this.res.includes("no90")) {
          this.text += 'No baixes suficientment. Flexiona més els genolls. ';
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
    else if(this.res.includes("bad")) {
      if(this.res.length == 1) {
        this.text = "Sembla que està bé, però pot haver-hi un error en la manera que l'has gravat. Si us plau, torna'l a fer de nou.";
      }
      else {
        if(this.res.includes("no90")) {
          this.text += 'No baixes suficientment. Flexiona més els genolls. ';
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
    document.getElementById("name").innerHTML = this.text
  }

  ngOnInit() {
  }

  onChange(event) {
    this.file = event.target.files[0];
    // console.log(this.file.name)
  }

}




//   constructor(private http: HttpClient, private transfer: FileTransfer, private file: File) { }

//   fileTransfer: FileTransferObject = this.transfer.create();
  
//   // full example
// upload() {
//   let options: FileUploadOptions = {
//      fileKey: 'file',
//      fileName: 'video.mp4',
//      headers: {}
//   }

//   this.fileTransfer.upload('assets/video.mp4', 'http://127.0.0.1:3000/predict', options)
//    .then((data) => {
//      // success
//      console.log(data);
//    }, (err) => {
//      // error
//      console.log(err);
//    })
// }

  // runHttp() {
  //   // this.http.post<any>('http://127.0.0.1:3000/prova2', {Title: "aiushdisauhf"})
  //   //   .subscribe(data => {
  //   //     console.log(data);
  //   //   });

  //   const endpoint = 'http://127.0.0.1:3000/predict';
  //   const formData: FormData = new FormData();
  //   this.fileToUpload 
  //   formData.append('fileKey', 'assets/video.mp4', 'video.mp4');
  //   this.http.post<any>(endpoint, formData)
  //     .subscribe(data => {
  //       console.log(data);
  //     });
  //   // this.http.get<any>('http://127.0.0.1:3000/prova')
  //   //   .subscribe(data => {
  //   //     console.log(data);
  //   //   });
  // }