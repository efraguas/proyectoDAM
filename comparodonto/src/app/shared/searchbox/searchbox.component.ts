import {Component,EventEmitter,Input, Output} from '@angular/core';
import {FormControl} from '@angular/forms';

@Component({
  selector: 'shared-searchbox',
  standalone: true,
  imports: [],
  templateUrl: './searchbox.component.html',
  styleUrl: './searchbox.component.css'
})
export class SearchboxComponent {

  @Output()
  public onValue : EventEmitter<string> = new EventEmitter<string>();

  emitValue (value : string) : void {
    this.onValue.emit(value);
  }


}
