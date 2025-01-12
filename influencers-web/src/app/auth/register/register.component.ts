import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../shared/services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
})
export class RegisterComponent {
  username = '';
  password = '';
  confirmPassword = '';
  showSuccessModal = false;

  constructor(private authService: AuthService, private router: Router) {}

  onSignUp() {
    if (this.password !== this.confirmPassword) {
      console.error('Passwords do not match');
      return;
    }

    this.authService.signUp(this.username, this.password).subscribe(
      (response) => {
        console.log('Sign-up successful:', response);
        this.showSuccessModal = true;
      },
      (error) => {
        console.error('Sign-up error:', error);
      }
    );
  }

  goToLogin() {
    this.showSuccessModal = false;
    this.router.navigate(['/auth/login']);
  }
}
