import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../shared/services/auth.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  standalone: true,
  imports: [RouterModule, FormsModule],
})
export class LoginComponent {
  username: string = '';
  password: string = '';

  constructor(private authService: AuthService, private router: Router) {}


  onLogin(): void {
    if (!this.username || !this.password) {
      console.error('Username and password are required');
      return;
    }
  
    this.authService.login(this.username, this.password).subscribe(
      (response) => {
        console.log('Login successful:', response);
        localStorage.setItem('token', response.access_token);
        this.router.navigate(['/dashboard']);
      },
      (error) => {
        console.error('Login error:', error);
      }
    );
  }
  

  /**
   * Método para regresar a la página principal.
   */
  goToHome(): void {
    this.router.navigate(['/home']);
  }
}
