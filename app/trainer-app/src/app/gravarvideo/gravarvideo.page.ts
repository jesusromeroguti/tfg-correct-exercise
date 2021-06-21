import { Component, OnInit } from '@angular/core';

import { File } from '@ionic-native/file';
import { VideoCapturePlus, VideoCapturePlusOptions, MediaFile } from '@ionic-native/video-capture-plus/ngx';
import { ViewChild } from '@angular/core';



@Component({
  selector: 'app-gravarvideo',
  templateUrl: './gravarvideo.page.html',
  styleUrls: ['./gravarvideo.page.scss'],
})
export class GravarvideoPage {

  constructor(private videoCapturePlus: VideoCapturePlus) { }

 
  
  // @ViewChild('videoElement') videoElement: any;  
  // video: any;

  // initCamera(config:any) {
  //   var browser = <any>navigator;

  //   browser.getUserMedia = (browser.getUserMedia ||
  //     browser.webkitGetUserMedia ||
  //     browser.mozGetUserMedia ||
  //     browser.msGetUserMedia);

  //   browser.mediaDevices.getUserMedia(config).then(stream => {
  //     this.video.src = window.URL.createObjectURL(stream);
  //     this.video.play();
  //   });
  // }

  // recordVideo(){
  //   this.initCamera({ video: true, audio: false });
  // }

  // ngOnInit() {
  //   this.video = this.videoElement.nativeElement;
  // }
}
