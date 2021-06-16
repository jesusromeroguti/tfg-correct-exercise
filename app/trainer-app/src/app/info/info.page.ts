import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-info',
  templateUrl: './info.page.html',
  styleUrls: ['./info.page.scss'],
})
export class InfoPage {

  public items: any = [];

  constructor() {
    this.items = [
      { titol:"Com funciona", text: "Hola que tal", expanded: false },
      { titol:"Tecnologies usades", text: "Sosi maquina", expanded: false },
      { titol:"Perquè els vídeos tenen requisits", text: "Aleix maquina", expanded: false },
      { titol:"Som uns màquins challenge", text: "", expanded: false },
    ];
  }

  expandItem(item): void {
    if (item.expanded) {
      item.expanded = false;
    } else {
      this.items.map(listItem => {
        if (item == listItem) {
          listItem.expanded = !listItem.expanded;
        } else {
          listItem.expanded = false;
        }
        return listItem;
      });
    }
  }


}
