import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'formatFollowers',
  standalone: true,
})
export class FormatFollowersPipe implements PipeTransform {
  transform(value: number): string {

    return value >= 1000000
      ? `${(value / 1000000).toFixed(1)}M`
      : value >= 1000
      ? `${(value / 1000).toFixed(1)}K`
      : value.toString();
  }
}
