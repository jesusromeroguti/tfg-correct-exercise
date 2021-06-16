import { Component, OnInit } from '@angular/core';

import { File } from '@ionic-native/file';
import { MediaCapture, MediaFile, CaptureError } from '@ionic-native/media-capture/ngx';

@Component({
  selector: 'app-gravarvideo',
  templateUrl: './gravarvideo.page.html',
  styleUrls: ['./gravarvideo.page.scss'],
})
export class GravarvideoPage implements OnInit {

  private mediaCapture: MediaCapture = null;
  private file: File = null;

  constructor() { }

  ngOnInit() {
  }

  recordVideo() {
    this.mediaCapture.captureVideo().then(
      (data: MediaFile[]) => {
        console.log(data);
      },
      (err: CaptureError) => console.error(err)
    );
  }
}
