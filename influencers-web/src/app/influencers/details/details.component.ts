import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { InfluencersService } from '../../shared/services/influencers.service';
import { ClaimsService } from '../../shared/services/claims.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-details',
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.css'],
  standalone: true,
    imports: [CommonModule]
})
export class DetailsComponent implements OnInit {
  influencer: any = {};
  claims: any[] = [];

  constructor(
    private route: ActivatedRoute,
    private influencersService: InfluencersService,
    private claimsService: ClaimsService
  ) {}

  ngOnInit(): void {
    const influencerId = this.route.snapshot.paramMap.get('id');
    if (influencerId) {
      this.loadInfluencerDetails(+influencerId);
      this.loadClaimsForInfluencer(+influencerId);
    }
  }
  
  private loadInfluencerDetails(id: number): void {
    this.influencersService.getInfluencerById(id.toString()).subscribe( 
      (data) => {
        this.influencer = data || {};
      },
      (error) => {
        console.error('Error fetching influencer details:', error);
      }
    );
  }
  
  private loadClaimsForInfluencer(influencerId: number): void {
    this.influencersService.getClaimsByInfluencerId(influencerId.toString()).subscribe(
      (data) => {
        this.claims = data.claims || [];
        this.processClaims();
      },
      (error) => {
        console.error('Error fetching claims:', error);
      }
    );
  }
  

  private processClaims(): void {
    this.claims.forEach((claim) => {
      this.claimsService.processClaim(claim.claim_text).subscribe(
        (response) => {
          claim.verification = response.processed_claims[0]?.verification || 'No verification available';
        },
        (error) => {
          console.error('Error processing claim:', error);
          claim.verification = 'Error processing claim';
        }
      );
    });
  }
}
