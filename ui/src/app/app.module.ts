import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavComponent } from './nav/nav.component';
import { HomeComponent } from './home/home.component';
import { AmplifyService } from 'aws-amplify-angular';
import { HttpClientModule } from '@angular/common/http';
import { AmplifyAngularModule, AmplifyIonicModule} from 'aws-amplify-angular'
import { AuthGuardService } from './auth-guard.service';
import { MatTabsModuleComponent } from './mat-tabs-module/mat-tabs-module.component';
import { MatTabsModule } from '@angular/material';

@NgModule({
  declarations: [
    AppComponent,
    NavComponent,
    HomeComponent,
    MatTabsModuleComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    AmplifyAngularModule, 
    AmplifyIonicModule,
    MatTabsModule   
  ],
  providers: [AmplifyService, AuthGuardService],
  bootstrap: [AppComponent]
})
export class AppModule { }
