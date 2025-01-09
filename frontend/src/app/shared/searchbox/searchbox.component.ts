import {Component,EventEmitter, Output} from '@angular/core';

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
  @Output()
  public onClick : EventEmitter<string> = new EventEmitter<string>();

  emitValue (value : string) : void {
    this.onValue.emit(value);
    this.onClick.emit(value);
  }


}
