import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private baseUrl = `${environment.apiUrl}/auth`;

  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<any> {
    const body = JSON.stringify({ username, password });
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
    return this.http.post(`${this.baseUrl}/login`, body, { headers });
  }

  signUp(username: string, password: string): Observable<any> {
    const url = `${this.baseUrl}/register`;
    const body = { username, password };
    return this.http.post<any>(url, body, {
      headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
    });
  }


  getToken(): string | null {
    return localStorage.getItem('token');
  }


  logout(): void {
    localStorage.removeItem('token');
  }


  isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }
}
