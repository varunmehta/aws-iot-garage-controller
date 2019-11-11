
import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError} from 'rxjs/operators';
import { ChangeDetectionStrategy } from '@angular/compiler/src/core';
import { AmplifyService } from "aws-amplify-angular";
import { Router } from "@angular/router";
import { MatTabsModule } from '@angular/material';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
  
})
export class HomeComponent implements OnInit {
  
  username: string;
  todos: any[];
  constructor(private http: HttpClient,private amplifyService: AmplifyService, private _router: Router) {
    this.amplifyService
      .auth()
      .currentAuthenticatedUser()
      .then(user => {
        this.username = user.username;
      });
   }
  title = 'Open Sesame';
  status = ''
  logs = []
  httpOptions = {
    headers: new HttpHeaders({
      'Access-Control-Allow-Origin': '*',
      // 'Access-Control-Allow-Methods': 'OPTIONS,POST',
      // 'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
      'Content-Type': 'text/plain'
    })
  }
  ngOnInit() {
    this.setStatus();
    this.setLogs();
  }
  garage_url = 'https://v6naxj1ttk.execute-api.us-east-1.amazonaws.com/deploy/garage';
  logs_url = 'https://v6naxj1ttk.execute-api.us-east-1.amazonaws.com/deploy/logs';
  setLogs() {
    const response = this.getLogs().subscribe(
      (logs) => {
        let cleaned_logs = []
        for(const log of logs){
          console.log("ENTRY:")
          console.log(log)
          const dateAndTime = log['received_timestamp'].split(',')
          cleaned_logs.push({
            'status': log['status'],
            'date': dateAndTime[0].trim(),
            'time': dateAndTime[1].trim().split('.')[0] + " UTC"
          });
        }
        this.logs = cleaned_logs;
      }
    );
  }
  garageOpener(type) {
    if(type == "open"){
      this.status = "Your garage is now opening"
    }
    if(type == "close"){
      this.status = "Your garage is now closing"
    }
    this.postGarage({action: type}).subscribe(
      (val) => {
        console.log("POST call successful value returned in body", val);
        },
        response => {
            console.log("POST call in error", response);
        },
        () => {
            console.log("The POST observable is now completed.");
        }
    );
  }

  setStatus() {
    const response = this.getGarage().subscribe(
      (val) => {
        if(val['status'] == "CLOSE"){
          this.status = "Your garage is CLOSED"
        }
        else if(val['status'] == "OPEN"){
          this.status = "Your garage is OPEN"
        }
        else if(val['status'] == "LONG_OPEN"){
          this.status = "Your garage has been OPEN FOR A WHILE!!"
        }
        console.log("GET call successful value returned in body", val);
        },
        response => {
            console.log("GET call in error", response);
        },
        () => {
            console.log("The GET observable is now completed.");
        }
    );
    console.log("Response: ", response)
  }

  postGarage(payload: { 'action': string; }): Observable<JSON> {
    console.log('Sending:', payload);
    return this.http.post<JSON>(this.garage_url, payload, this.httpOptions)
    .pipe(
      catchError(this.handleError)
    );
  }

  getLogs(): Observable<any[]> {
    return this.http.get<any[]>(this.logs_url, this.httpOptions)
    .pipe(
      catchError(this.handleError)
    )
  }

  getGarage(): Observable<JSON> {
    return this.http.get<JSON>(this.garage_url, this.httpOptions)
    .pipe(
      catchError(this.handleError)
    );
  }

  logOut() {
    this.amplifyService
      .auth()
      .signOut()
      .then(() => {
        this._router.navigateByUrl("");
      })
      .catch(err => {
        return false;
      });
  }


  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error.message);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      // console.error(
      //   `Backend returned code ${error.status}, ` +
      //   `body was: ${error.error}`);
    }
    // return an observable with a user-facing error message
    return throwError(
      'Something bad happened; please try again later.');
  }

}

