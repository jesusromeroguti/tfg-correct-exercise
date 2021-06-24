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
      { titol:"Com funciona?", text: "L'usuari s'ha de gravar realitzant una esquat (complint els requeriments), seguidament es puja el vídeo al servidor i retorna un resultat. El resultat explica si l'exercici està correctament fet o no i el perquè.", expanded: false },
      { titol:"Tecnologies utilitzades", text: "El model d'IA està construit amb les llibreries TensorFlow i Keras. L'API utilitza Flask i l'aplicació web/mòbil està implementada utilitzant la llibreria ionic sobre el framework Angular.", expanded: false },
      { titol:"Per què els vídeos tenen requisits?", text: "Perquè el model d'IA està entrenat amb un conjunt de vídeos complint aquests mateixos requeriments. Això és perquè entrenar un model sense uns requisits suposa complicar molt el procés d'aprenentatge.", expanded: false },
      { titol:"Com funciona la IA per resoldre aquest problema?", text: "El model està entrenat amb vídeos de persones fent esquats correctament i incorrectament. L'arquitectura del model, després del procés d'entrenament, ha aconseguit inferir les relacions i patrons existents en l'execució correcta d'un esquat i d'aquesta manera és capaç de detectar si està bé o no.", expanded: false },
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
