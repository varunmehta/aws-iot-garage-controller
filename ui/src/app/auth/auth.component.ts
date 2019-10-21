import { Component, OnInit } from '@angular/core';
import {AmplifyService} from 'aws-amplify-angular';
import {Router} from '@angular/router';
@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.css']
})
export class AuthComponent implements OnInit {

  constructor(private amplifyService:AmplifyService, private _router: Router ) { 
    this.amplifyService = amplifyService;
    this.amplifyService.authStateChange$.subscribe(authState =>{
      if(authState.state ==="signedIn"){
        this._router.navigateByUrl("/home");
      }
    })
  }

  ngOnInit() {
  //  const URL="https://iot-app.auth.us-east-1.amazoncognito.com/login?response_type=code&client_id=51ss0jtm15b0p3fdrqil33e2ff&redirect_uri=http://localhost:4200" 
  // window.location.assign(URL);
  }

}
