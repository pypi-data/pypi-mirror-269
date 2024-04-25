/*
 *  Copyright 2017 TWO SIGMA OPEN SOURCE, LLC
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *         http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

import $ from 'jquery';
import * as _ from 'underscore';

import { Widget } from '@lumino/widgets';
import { Message, MessageLoop } from '@lumino/messaging';

import { OtherOptionsWidgetInterface } from './OtherOptionsWidgetInterface';
import { IOtherJVMOptions } from '../../../utils/api';
import { OtherOptionsChangedMessage, SizeChangedMessage } from '../../Messages';

export class OtherOptionsWidget extends Widget implements OtherOptionsWidgetInterface {
  public readonly ADD_BUTTON_SELECTOR = '#add_option_jvm_sett';
  public readonly PANEL_SELECTOR = '#other_property';

  public readonly HTML_ELEMENT_TEMPLATE = `
<fieldset>
  <div class="bx-panel">
    <div class="bx-panel-heading">
    
      Other Command Line Options
    
      <button type="button"
        id="add_option_jvm_sett"
        class="bx-btn">
        <i class="fa fa-plus"></i>
      </button>

    </div>
    
    <div id="other_property" class="bx-panel-body"></div>
  </div>
</fieldset>
`;

  public get $node(): JQuery<HTMLElement> {
    return $(this.node);
  }

  constructor() {
    super();

    $(this.HTML_ELEMENT_TEMPLATE).appendTo(this.node);
    this.$node.find(this.ADD_BUTTON_SELECTOR).on('click', this.addOptionButtonClickedHandler.bind(this));
  }

  private clear() {
    this._options = [];
    this.$node.find(this.PANEL_SELECTOR).empty();
    MessageLoop.sendMessage(this.parent, new SizeChangedMessage());
  }

  public onLoad(otherOptions: IOtherJVMOptions) {
    this.clear();
    for (const option of otherOptions) {
      this.addFormElement(option);
    }
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  private addOptionButtonClickedHandler(evt) {
    this.addFormElement();
  }

  private createFormRowElement(): JQuery<HTMLElement> {
    return $('<div>', {
      class: 'bx-form-row',
    });
  }

  private createInputElement(val = ''): JQuery<HTMLElement> {
    return $('<input>', {
      class: 'bx-input-text',
      type: 'text',
      placeholder: 'value',
    })
      .val(val)
      .data('val', val);
  }

  private createRemoveButtonElement(): JQuery<HTMLElement> {
    return $('<button>', {
      type: 'button',
      class: 'bx-btn',
    }).append($('<i>', { class: 'fa fa-times' }));
  }

  private addFormElement(value = ''): void {
    const element = this.createFormRowElement()
      .append(this.createInputElement(value))
      .append(this.createRemoveButtonElement());
    element.appendTo(this.$node.find(this.PANEL_SELECTOR));

    MessageLoop.sendMessage(this, new ElementAddedMessage(element));
    MessageLoop.sendMessage(this.parent, new SizeChangedMessage());
  }

  public processMessage(msg: Message): void {
    switch (msg.type) {
      case TYPE_ELEMENT_ADDED:
        this.onElementAdded(msg as ElementAddedMessage);
        break;
      case TYPE_ELEMENT_REMOVED:
        this.onElementRemoved(msg as ElementRemovedMessage);
        break;
      default:
        super.processMessage(msg);
    }
  }

  private onElementAdded(msg: ElementAddedMessage): void {
    const el = msg.element;
    el.find('button').on('click', { el: el }, this.removeOptionButtonClickedHandler.bind(this));
    const input = el.find('input');
    input.on('keyup', _.debounce(this.inputChangedHandler.bind(this), 1000));
    this.addOption(input.val().toString());
  }

  private onElementRemoved(msg: ElementRemovedMessage): void {
    const el = msg.element;
    const option = el.find('input').val().toString();
    this.removeOption(option);
  }

  private removeOptionButtonClickedHandler(evt) {
    const el: JQuery<HTMLElement> = evt.data.el;
    el.remove();
    MessageLoop.sendMessage(this, new ElementRemovedMessage(el));
    MessageLoop.sendMessage(this.parent, new SizeChangedMessage());
  }

  private inputChangedHandler(evt): void {
    const el = $(evt.currentTarget);
    const prev = el.data('val');
    const curr = `${el.val()}`;
    el.data('val', curr);
    if ('' === prev) {
      this.addOption(curr);
      return;
    }
    if ('' === curr) {
      this.removeOption(prev);
      return;
    }
    this.changeOption(prev, curr);
  }

  private _options: IOtherJVMOptions = [];

  private addOption(option: string): void {
    if ('' === option) {
      return;
    }

    this._options.push(option);
    this.optionsChanged();
  }

  private removeOption(option): void {
    if ('' === option) {
      return;
    }
    const index = this._options.indexOf(option);
    if (-1 === index) {
      return;
    }
    this._options.splice(index, 1);
    this.optionsChanged();
  }

  private changeOption(from, to): void {
    const index = this._options.indexOf(from);
    this._options[index] = to;
    this.optionsChanged();
  }

  private optionsChanged() {
    const msg = new OtherOptionsChangedMessage(this._options);
    MessageLoop.sendMessage(this.parent, msg);
  }
}

const TYPE_ELEMENT_ADDED = 'element-added';

class ElementAddedMessage extends Message {
  constructor(element: JQuery<HTMLElement>) {
    super(TYPE_ELEMENT_ADDED);
    this._element = element;
  }

  public get element(): JQuery<HTMLElement> {
    return this._element;
  }

  private _element: JQuery<HTMLElement>;
}

const TYPE_ELEMENT_REMOVED = 'element-removed';

class ElementRemovedMessage extends Message {
  constructor(element: JQuery<HTMLElement>) {
    super(TYPE_ELEMENT_REMOVED);
    this._element = element;
  }

  public get element(): JQuery<HTMLElement> {
    return this._element;
  }

  private _element: JQuery<HTMLElement>;
}
