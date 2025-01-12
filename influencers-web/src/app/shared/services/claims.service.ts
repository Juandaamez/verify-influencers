import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class ClaimsService {
  private baseUrl = `${environment.apiUrl}/claims`;

  constructor(private http: HttpClient) {}

  processClaim(claimText: string): Observable<any> {
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    });
    const body = { text: claimText };
    return this.http.post<any>(`${this.baseUrl}/process`, body, { headers });
  }
}
