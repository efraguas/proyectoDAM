import {Component, EventEmitter, Output} from '@angular/core';
import {FormControl, ReactiveFormsModule} from '@angular/forms';

@Component({
  selector: 'select-box',
  standalone: true,
  imports: [
    ReactiveFormsModule
  ],
  templateUrl: './select-box.component.html',
  styleUrl: './select-box.component.css'
})
export class SelectBoxComponent {

  public selector: FormControl<string | null> = new FormControl<string | null>('nombre');

  @Output() changeSelection: EventEmitter<string | null> = new EventEmitter<string | null>();


  emitSeleccion(): void {
    this.changeSelection.emit(this.selector.value);
  }

}
