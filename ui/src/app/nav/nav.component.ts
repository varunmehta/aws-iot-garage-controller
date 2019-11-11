import { Component, OnInit } from '@angular/core';
import { AmplifyService } from "aws-amplify-angular";
import { Router } from "@angular/router";

@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.scss']
})

export class NavComponent implements OnInit {
 
  // constructor(private amplifyService: AmplifyService, private _router: Router) {
  //   this.amplifyService = amplifyService;

  //   this.amplifyService.authStateChange$.subscribe(authState => {
  //     if (authState.state === "signedIn") {
  //       this._router.navigateByUrl("/home");
  //     }
  //   });
  constructor(private amplifyService: AmplifyService, private _router: Router) {
    this.amplifyService = amplifyService;

    this.amplifyService.authStateChange$.subscribe(authState => {
      if (authState.state === "signedIn") {
        this._router.navigateByUrl("/home");
      }
      return false;
    });
  }

  ngOnInit() {}
  }

  // ngOnInit() {
  //   // const URL = "https://open-sesame.auth.us-east-1.amazoncognito.com/login?response_type=code&client_id=3lieofj6vem78nb9u5n5jvbrra&redirect_uri=http://localhost:4200"
  //   // window.location.assign(URL);
  // }
  // onLoginClick() {
  //   const URL = "https://open-sesame.auth.us-east-1.amazoncognito.com/login?response_type=code&client_id=3lieofj6vem78nb9u5n5jvbrra&redirect_uri=http://localhost:4200"
  //   window.location.assign(URL);
  // }
 
// }
