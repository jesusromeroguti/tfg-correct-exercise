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
  res = null
  text = ''
  
  upload(){

    // Create form data
    const formData = new FormData();     
      
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
    }, (err) => {
      console.log(err);
    });

  }

  tractarCodi() {
    if(this.res.includes("good") && this.res.length === 1) {
      this.text = 'Ets el puto amo';
    }
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