import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SearchService } from '../../shared/services/search.service';
import { InfluencersService } from '../../shared/services/influencers.service';

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule],
  selector: 'app-search',
  templateUrl: './search.component.html',
})
export class SearchComponent {
  searchQuery: string = '';
  influencer: any = null;
  claims: any[] = [];
  showModal: boolean = false;

  constructor(
    private searchService: SearchService,
    private influencersService: InfluencersService
  ) {}


  searchInfluencer(): void {
    if (!this.searchQuery.trim()) {
      alert('Please enter a name to search.');
      return;
    }

    const requestBody = { name: this.searchQuery };

    this.searchService.searchInfluencer(requestBody).subscribe({
      next: (response) => {
        if (response?.influencer_id) {
          const influencerId = response.influencer_id.toString();
          this.fetchInfluencerDetails(influencerId);
          this.showModal = true;
        } else {
          console.error('Error: Influencer ID not found in response:', response);
          alert('The influencer was not found or there was an error.');
        }
      },
      error: (err) => {
        console.error('Error searching influencer:', err);
        alert('An error occurred while searching for the influencer.');
      },
    });
  }


  fetchInfluencerDetails(id: string): void {
    this.influencersService.getInfluencerById(id).subscribe({
      next: (details) => {
        this.influencer = details.influencer || null;
        this.claims = details.claims || [];
      },
      error: (err) => {
        console.error('Error fetching influencer details:', err);
        alert('An error occurred while fetching influencer details.');
      },
    });
  }


  closeModal(): void {
    this.showModal = false;
  }
}
