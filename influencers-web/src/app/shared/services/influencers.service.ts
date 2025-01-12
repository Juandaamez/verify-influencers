import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class InfluencersService {
  private baseUrl = `${environment.apiUrl}/influencers`;

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('Authentication token not found in localStorage.');
      throw new Error('Authentication required. Please log in.');
    }
    return new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    });
  }

  getLeaderboard(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/leaderboard`, { headers: this.getHeaders() });
  }

  getInfluencerById(id: string): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/${id}`, { headers: this.getHeaders() });
  }

  getClaimsByInfluencerId(id: string): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/${id}/claims`, { headers: this.getHeaders() });
  }

  searchInfluencer(body: { name: string }): Observable<any> {

    const headers = this.getHeaders();
    return this.http.post(`${this.baseUrl}/search`, body, { headers });
  }
}
