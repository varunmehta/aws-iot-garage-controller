import { NgModule, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Auth, AuthClass } from 'aws-amplify';
import { RouterModule, Routes } from '@angular/router';
import {AuthComponent} from "src/app/auth/auth.component";
import { HomeComponent } from './home/home.component';
import { AuthGuardService } from './auth-guard.service';

const routes: Routes = [
  {path: "", component:AuthComponent},
  {path: "home", component: HomeComponent},
  {path:"**", redirectTo:""}
]

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    RouterModule.forRoot(routes)
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
