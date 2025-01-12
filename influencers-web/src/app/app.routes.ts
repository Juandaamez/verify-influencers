import { Routes } from '@angular/router';
import { HomeComponent } from './welcome/home/home.component';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import { MainComponent } from './dashboard/main/main.component';

export const appRoutes: Routes = [
  {
    path: '',
    component: HomeComponent,
  },
  {
    path: 'auth/login',
    component: LoginComponent,
  },
  {
    path: 'auth/register',
    component: RegisterComponent,
  },
  {
    path: 'dashboard',
    component: MainComponent,
    children: [
      {
        path: 'influencers',
        loadChildren: () =>
          import('./influencers/influencers-routing.module').then(
            (m) => m.InfluencersRoutingModule
          ),
      },
      {
        path: 'influencers/search',
        component: RegisterComponent,
      },
    ],
  },
  {
    path: '**',
    redirectTo: '',
  },
];
