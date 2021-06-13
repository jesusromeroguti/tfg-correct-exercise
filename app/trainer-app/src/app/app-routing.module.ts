import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'inici',
    pathMatch: 'full'
  },
  {
    path: 'inici',
    loadChildren: () => import('./inici/inici.module').then( m => m.IniciPageModule)
  },
  {
    path: 'pujarvideo',
    loadChildren: () => import('./pujarvideo/pujarvideo.module').then( m => m.PujarvideoPageModule)
  },
  {
    path: 'gravarvideo',
    loadChildren: () => import('./gravarvideo/gravarvideo.module').then( m => m.GravarvideoPageModule)
  },
  {
    path: 'info',
    loadChildren: () => import('./info/info.module').then( m => m.InfoPageModule)
  },
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
