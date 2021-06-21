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
      { titol:"Com funciona", text: "L'usuari s'ha de gravar realitzant una esquat (complint els requeriments), seguidament es puja el vídeo al servidor i retorna un resultat. El resultat explica si l'exercici està correctament fet o no i el perquè.", expanded: false },
      { titol:"Tecnologies utilitzades", text: "El model d'IA està construit amb les llibreries TensorFlow i Keras. L'API utilitza Flask i l'aplicació web/mòbil està implementada utilitzant la llibreria ionic sobre el framework Angular.", expanded: false },
      { titol:"Perquè els vídeos tenen requisits", text: "Perquè el model d'IA està entrenat amb un conjunt de vídeos complint aquets mateixos requeriments. Això es perquè entrenar un model sense uns requisits suposa complicar molt el procés d'aprenentatge.", expanded: false },
      { titol:"Com funciona la IA per resoldre aquest problema", text: "El model està entrenat amb vídeos de persones fent esquats correcta i incorrectament. L'arquitectura del model despres del procès d'entrenament ha conseguit inferir les relacions i patrons existent en la execució correcta d'una esquat i d'aquesta manera es capaç de detectar si està be o no.", expanded: false },
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
