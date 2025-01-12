import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { InfluencersService } from '../../shared/services/influencers.service';
import { FormatFollowersPipe } from '../../shared/pipes/format-followers.pipe';

@Component({
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.css'],
  standalone: true,
  imports: [CommonModule, RouterModule, FormatFollowersPipe],
})
export class ListComponent implements OnInit {
  influencers: any[] = [];
  statistics = {
    active_influencers: 0,
    claims_verified: 0,
    average_trust_score: 0,
  };

  constructor(
    private influencersService: InfluencersService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadLeaderboard();
  }

  loadLeaderboard(): void {
    this.influencersService.getLeaderboard().subscribe((data: any) => {
      this.influencers = data.leaderboard;
      this.statistics = data.statistics;
    });
  }

  navigateToDetails(id: number): void {
    this.router.navigate([`/dashboard/influencers/details/${id}`]);
  }
}
